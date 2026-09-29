"""
Camada de persistência (SQLite) do UrutauLLM-Lab.

Serve auth (#7), scoreboard (#5) e métricas de challenge (#9) a partir de um
único arquivo SQLite. Zero infra: um arquivo, stdlib `sqlite3`, conexão por
request via `flask.g`.

Tabelas:
  users       — identidade leve (username sem senha, pra workshops/demos)
  attempts    — uma linha por tentativa em /api/chat (com flag de sucesso)
  hint_views  — uma linha cada vez que um usuário abre a dica de um challenge

Scoreboard e métricas são DERIVADOS dessas tabelas (nada é duplicado).
"""

import os
import sqlite3
import logging
from flask import g

logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DATABASE_PATH", "data/urutau.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS attempts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER,
    challenge_id TEXT NOT NULL,
    success      INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS hint_views (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER,
    challenge_id TEXT NOT NULL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_attempts_challenge ON attempts(challenge_id);
CREATE INDEX IF NOT EXISTS idx_attempts_user      ON attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_hint_challenge     ON hint_views(challenge_id);
"""


def get_db() -> sqlite3.Connection:
    """Conexão SQLite por request (cacheada em flask.g)."""
    if "db" not in g:
        os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


def close_db(exception=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Cria o schema (idempotente). Roda fora do ciclo de request."""
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
    logger.info(f"SQLite pronto em {DB_PATH}")


def init_app(app) -> None:
    """Registra teardown e garante o schema no boot."""
    app.teardown_appcontext(close_db)
    init_db()


# --------------------------------------------------------------------------
# Users / auth (#7)
# --------------------------------------------------------------------------
def get_or_create_user(username: str) -> dict:
    """Retorna o usuário (criando se necessário). Username sem senha."""
    username = (username or "").strip()
    if not username:
        raise ValueError("username vazio")
    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO users (username) VALUES (?)", (username,)
    )
    db.commit()
    row = db.execute(
        "SELECT id, username, created_at FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    return dict(row)


def get_user(user_id: int) -> dict | None:
    db = get_db()
    row = db.execute(
        "SELECT id, username, created_at FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    return dict(row) if row else None


# --------------------------------------------------------------------------
# Attempts (#5 scoreboard, #9 metrics)
# --------------------------------------------------------------------------
def record_attempt(user_id, challenge_id: str, success: bool) -> None:
    db = get_db()
    db.execute(
        "INSERT INTO attempts (user_id, challenge_id, success) VALUES (?, ?, ?)",
        (user_id, challenge_id, 1 if success else 0),
    )
    db.commit()


def record_hint_view(user_id, challenge_id: str) -> None:
    db = get_db()
    db.execute(
        "INSERT INTO hint_views (user_id, challenge_id) VALUES (?, ?)",
        (user_id, challenge_id),
    )
    db.commit()


# --------------------------------------------------------------------------
# Scoreboard (#5)
# --------------------------------------------------------------------------
def scoreboard() -> list[dict]:
    """Ranking: por usuário, nº de challenges resolvidos (distintos) e tempo
    total (do primeiro attempt ao primeiro sucesso de cada challenge)."""
    db = get_db()
    rows = db.execute(
        """
        WITH solves AS (
            SELECT
                a.user_id,
                a.challenge_id,
                MIN(CASE WHEN a.success = 1 THEN a.created_at END) AS solved_at,
                MIN(a.created_at) AS first_seen
            FROM attempts a
            WHERE a.user_id IS NOT NULL
            GROUP BY a.user_id, a.challenge_id
        )
        SELECT
            u.username,
            COUNT(s.solved_at) AS solved,
            COALESCE(SUM(
                CASE WHEN s.solved_at IS NOT NULL
                     THEN (julianday(s.solved_at) - julianday(s.first_seen)) * 86400
                END
            ), 0) AS total_seconds
        FROM users u
        LEFT JOIN solves s ON s.user_id = u.id
        GROUP BY u.id
        HAVING solved > 0
        ORDER BY solved DESC, total_seconds ASC
        """
    ).fetchall()
    return [
        {
            "username": r["username"],
            "solved": r["solved"],
            "total_seconds": round(r["total_seconds"], 1),
        }
        for r in rows
    ]


# --------------------------------------------------------------------------
# Per-challenge quality metrics (#9)
# --------------------------------------------------------------------------
def challenge_stats(challenge_id: str) -> dict:
    """Métricas de qualidade de um challenge, derivadas de attempts/hint_views."""
    db = get_db()

    total_attempts = db.execute(
        "SELECT COUNT(*) c FROM attempts WHERE challenge_id = ?", (challenge_id,)
    ).fetchone()["c"]

    unique_users = db.execute(
        "SELECT COUNT(DISTINCT user_id) c FROM attempts "
        "WHERE challenge_id = ? AND user_id IS NOT NULL",
        (challenge_id,),
    ).fetchone()["c"]

    solvers = db.execute(
        "SELECT COUNT(DISTINCT user_id) c FROM attempts "
        "WHERE challenge_id = ? AND success = 1 AND user_id IS NOT NULL",
        (challenge_id,),
    ).fetchone()["c"]

    hint_views = db.execute(
        "SELECT COUNT(*) c FROM hint_views WHERE challenge_id = ?", (challenge_id,)
    ).fetchone()["c"]

    # média de tentativas até o primeiro sucesso (só quem resolveu)
    avg_attempts_to_solve = db.execute(
        """
        SELECT AVG(n) v FROM (
            SELECT COUNT(*) n
            FROM attempts a
            JOIN (
                SELECT user_id, MIN(created_at) solved_at
                FROM attempts
                WHERE challenge_id = ? AND success = 1 AND user_id IS NOT NULL
                GROUP BY user_id
            ) s ON s.user_id = a.user_id
            WHERE a.challenge_id = ? AND a.created_at <= s.solved_at
            GROUP BY a.user_id
        )
        """,
        (challenge_id, challenge_id),
    ).fetchone()["v"]

    success_rate = round(solvers / unique_users, 3) if unique_users else 0.0
    # desistência: usuários que tentaram mas nunca resolveram
    abandonment_rate = (
        round(1 - (solvers / unique_users), 3) if unique_users else 0.0
    )

    return {
        "challenge_id": challenge_id,
        "total_attempts": total_attempts,
        "unique_users": unique_users,
        "solvers": solvers,
        "success_rate": success_rate,
        "abandonment_rate": abandonment_rate,
        "avg_attempts_to_solve": (
            round(avg_attempts_to_solve, 2) if avg_attempts_to_solve else None
        ),
        "hint_views": hint_views,
    }
