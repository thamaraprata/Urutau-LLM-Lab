"""
Testes de integração da API (#6) — usam flask.test_client, sem LLM real.

O LLMClient é mockado por fixture, então nenhum Ollama/OpenAI é necessário.
O banco aponta pra um SQLite temporário, isolado do data/urutau.db real.
"""

import os
import sys
import tempfile

import pytest

# Isola o banco ANTES de importar o app (DB_PATH é lido no import de llm.db).
_TMP_DB = os.path.join(tempfile.mkdtemp(), "test_urutau.db")
os.environ["DATABASE_PATH"] = _TMP_DB
os.environ.setdefault("SECRET_KEY", "test-secret")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app as appmod  # noqa: E402


@pytest.fixture
def client(monkeypatch):
    """Test client com o LLM mockado (retorna a mensagem ecoada por padrão)."""
    appmod.app.config["TESTING"] = True

    def fake_chat(message, system_prompt=None):
        return f"echo: {message}"

    monkeypatch.setattr(appmod.llm_client, "chat", fake_chat)
    with appmod.app.test_client() as c:
        yield c


def solve(client, challenge_id, flag):
    """Faz o LLM 'vazar' a flag pra simular um solve."""
    appmod.llm_client.chat = lambda m, system_prompt=None: f"pwned: {flag}"
    return client.post(
        "/api/chat", json={"message": "exploit", "challenge_id": challenge_id}
    )


# ---- endpoints básicos -----------------------------------------------------
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_index_renders(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"UrutauLLM-Lab" in r.data or b"Urutau" in r.data


def test_security_headers_present(client):
    r = client.get("/health")
    assert "Content-Security-Policy" in r.headers
    assert r.headers["X-Frame-Options"] == "DENY"
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert "max-age" in r.headers["Strict-Transport-Security"]


def test_list_challenges(client):
    r = client.get("/api/challenges")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list) and len(data) >= 5
    assert {"id", "name", "owasp", "difficulty", "status"} <= set(data[0])


# ---- chat ------------------------------------------------------------------
def test_chat_empty_message(client):
    r = client.post("/api/chat", json={"message": "", "challenge_id": "01"})
    assert r.status_code == 400


def test_chat_flag_not_found(client):
    r = client.post("/api/chat", json={"message": "oi", "challenge_id": "01"})
    assert r.status_code == 200
    body = r.get_json()
    assert body["flag_found"] is False
    assert body["response"].startswith("echo:")


def test_chat_flag_found(client):
    r = solve(client, "01", "PWNED-2024")
    assert r.status_code == 200
    assert r.get_json()["flag_found"] is True


# ---- hint / writeup --------------------------------------------------------
def test_hint(client):
    r = client.get("/api/challenges/01/hint")
    assert r.status_code == 200
    assert "hint" in r.get_json()


def test_writeup(client):
    r = client.get("/api/challenges/01/writeup")
    assert r.status_code == 200
    assert "writeup" in r.get_json()


def test_hint_unknown_challenge(client):
    assert client.get("/api/challenges/zz/hint").status_code == 404


# ---- auth ------------------------------------------------------------------
def test_login_logout_me(client):
    assert client.get("/api/me").get_json()["username"] is None
    r = client.post("/login", json={"username": "tester"})
    assert r.status_code == 200 and r.get_json()["username"] == "tester"
    assert client.get("/api/me").get_json()["username"] == "tester"
    assert client.post("/logout").status_code == 200
    assert client.get("/api/me").get_json()["username"] is None


def test_login_rejects_bad_username(client):
    assert client.post("/login", json={"username": ""}).status_code == 400
    assert client.post("/login", json={"username": "x" * 33}).status_code == 400


# ---- scoreboard / stats ----------------------------------------------------
def test_scoreboard_reflects_solve(client):
    client.post("/login", json={"username": "champ"})
    solve(client, "02", "ACME-SECRET-LEAK-777")
    board = client.get("/api/scoreboard").get_json()
    assert any(row["username"] == "champ" and row["solved"] >= 1 for row in board)


def test_stats_endpoint(client):
    client.post("/login", json={"username": "analyst"})
    client.get("/api/challenges/01/hint")
    solve(client, "01", "PWNED-2024")
    s = client.get("/api/stats/01").get_json()
    assert s["challenge_id"] == "01"
    assert s["total_attempts"] >= 1
    assert s["hint_views"] >= 1
    assert 0.0 <= s["success_rate"] <= 1.0


def test_stats_unknown_challenge(client):
    assert client.get("/api/stats/zz").status_code == 404


def test_pages_render(client):
    assert client.get("/scoreboard").status_code == 200
    assert client.get("/dashboard").status_code == 200


def test_404_json(client):
    r = client.get("/does-not-exist")
    assert r.status_code == 404
    assert "error" in r.get_json()
