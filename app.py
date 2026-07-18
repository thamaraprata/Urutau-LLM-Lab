"""
UrutauLLM-Lab - Aplicação principal Flask
Lab de LLM Security com challenges CTF-style.
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv

from llm.client import LLMClient
from llm.challenges import ChallengeManager

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
