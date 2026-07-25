"""
UrutauLLM-Lab - Aplicação principal Flask
Lab de LLM Security com challenges CTF-style.
"""

import os
import logging
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv

from llm.client import LLMClient
from llm.challenges import ChallengeManager
from llm import db

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Inicializa Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
CORS(app)

# Inicializa clientes
llm_client = LLMClient()
challenge_manager = ChallengeManager()

# Inicializa a camada de persistência (SQLite: users/attempts/hint_views)
db.init_app(app)


def login_required(f):
    """Middleware de auth para endpoints sensíveis (ex.: admin/criação de
    challenges). Auth aqui é username-only, pensada pra workshops/demos."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Autenticação necessária"}), 401
        return f(*args, **kwargs)

    return wrapper


@app.after_request
def add_security_headers(response):
    """Headers de segurança HTTP (defense-in-depth).

    Nota didática: a app renderiza respostas do LLM via textContent (não
    innerHTML), então não há XSS refletido no front — mas uma CSP estrita é a
    rede de segurança contra improper output handling (ver challenge 05). O
    front é 100% same-origin (CSS/JS em /static), logo default-src 'self' basta.
    """
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
        "base-uri 'self'; frame-ancestors 'none'"
    )
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


@app.route("/")
def index():
    """Página principal com chat e lista de challenges."""
    challenges = challenge_manager.list_challenges()
    return render_template("index.html", challenges=challenges)


@app.route("/health")
def health():
    """Health check para Docker."""
    return jsonify(
        {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "llm_provider": os.getenv("LLM_PROVIDER", "ollama"),
        }
    )


@app.route("/login", methods=["POST"])
def login():
    """Login leve por username (sem senha) — pra workshops e scoreboard."""
    data = request.get_json(silent=True) or request.form
    username = (data.get("username") or "").strip()
    if not username or len(username) > 32:
        return jsonify({"error": "username inválido (1-32 chars)"}), 400
    try:
        user = db.get_or_create_user(username)
    except ValueError:
        return jsonify({"error": "username inválido"}), 400
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    logger.info(f"Login: {user['username']} (id={user['id']})")
    return jsonify({"username": user["username"], "id": user["id"]})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status": "logged_out"})


@app.route("/api/me", methods=["GET"])
def me():
    """Usuário atual da sessão (ou null) — usado pela UI."""
    if session.get("user_id"):
        return jsonify(
            {"username": session.get("username"), "id": session.get("user_id")}
        )
    return jsonify({"username": None, "id": None})


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Endpoint principal de chat.
    Recebe: {"message": "...", "challenge_id": "01"}
    Retorna: {"response": "...", "challenge_id": "01"}
    """
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Mensagem vazia"}), 400

        message = data.get("message", "").strip()
        challenge_id = data.get("challenge_id", "00")

        if not message:
            return jsonify({"error": "Mensagem vazia"}), 400

        # Log da mensagem (sem PII)
        logger.info(f"Chat - Challenge: {challenge_id} - Length: {len(message)}")

        # Pega o challenge (se for 00, é modo livre)
        challenge = challenge_manager.get_challenge(challenge_id)

        # Monta o system prompt baseado no challenge
        system_prompt = challenge["system_prompt"] if challenge else None

        # Chama o LLM
        response = llm_client.chat(message, system_prompt=system_prompt)

        # Verifica se o challenge foi completado
        flag_found = False
        if challenge and "flag_pattern" in challenge:
            flag_found = challenge["flag_pattern"].lower() in response.lower()

        return jsonify(
            {
                "response": response,
                "challenge_id": challenge_id,
                "flag_found": flag_found,
                "challenge_name": challenge["name"] if challenge else "Free Chat",
            }
        )

    except Exception as e:
        logger.error(f"Erro no chat: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500


@app.route("/api/challenges", methods=["GET"])
def list_challenges():
    """Lista todos os challenges disponíveis."""
    return jsonify(challenge_manager.list_challenges())


@app.route("/api/challenges/<challenge_id>/hint", methods=["GET"])
def get_hint(challenge_id):
    """Retorna uma dica para o challenge."""
    challenge = challenge_manager.get_challenge(challenge_id)
    if not challenge:
        return jsonify({"error": "Challenge não encontrado"}), 404
    return jsonify({"hint": challenge.get("hint", "Sem dica disponível")})


@app.route("/api/challenges/<challenge_id>/writeup", methods=["GET"])
def get_writeup(challenge_id):
    """Retorna o write-up do challenge (solução)."""
    challenge = challenge_manager.get_challenge(challenge_id)
    if not challenge:
        return jsonify({"error": "Challenge não encontrado"}), 404
    return jsonify({"writeup": challenge.get("writeup", "Sem write-up disponível")})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint não encontrado"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erro interno do servidor"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    logger.info(f"🦉 UrutauLLM-Lab iniciando na porta {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
