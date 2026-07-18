"""
Cliente LLM - Suporta Ollama (local) e OpenAI.
"""

import os
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)


class LLMClient:
    """Cliente unificado para diferentes providers de LLM."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()

        if self.provider == "ollama":
            self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            self.model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
            self._init_ollama()
        elif self.provider == "openai":
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY não configurada")
            self._init_openai()
        else:
            raise ValueError(f"Provider não suportado: {self.provider}")

        logger.info(f"LLM Client inicializado: {self.provider} / {self.model}")

    def _init_ollama(self):
        """Inicializa o cliente Ollama."""
        try:
            import ollama

            self.ollama_client = ollama.Client(host=self.host)
        except ImportError:
            logger.warning("Biblioteca ollama não instalada, usando requests")
            self.ollama_client = None

    def _init_openai(self):
        """Inicializa o cliente OpenAI."""
        try:
            from openai import OpenAI

            self.openai_client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("Execute: pip install openai")

    def chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """
        Envia mensagem para o LLM e retorna a resposta.

        Args:
            user_message: Mensagem do usuário
            system_prompt: System prompt (opcional, define comportamento)

        Returns:
            Resposta do LLM
        """
        if self.provider == "ollama":
            return self._chat_ollama(user_message, system_prompt)
        elif self.provider == "openai":
            return self._chat_openai(user_message, system_prompt)

        raise ValueError(f"Provider não suportado: {self.provider}")

    def _chat_ollama(self, user_message: str, system_prompt: Optional[str]) -> str:
        """Chat via Ollama."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        try:
            if self.ollama_client:
                response = self.ollama_client.chat(
                    model=self.model, messages=messages
                )
                return response["message"]["content"]

            # Fallback com requests
            response = requests.post(
                f"{self.host}/api/chat",
                json={"model": self.model, "messages": messages, "stream": False},
                timeout=60,
            )
            response.raise_for_status()
            return response.json()["message"]["content"]

        except Exception as e:
            logger.error(f"Erro no Ollama: {e}")
            return f"[ERRO] Não foi possível conectar ao Ollama: {e}"

    def _chat_openai(self, user_message: str, system_prompt: Optional[str]) -> str:
        """Chat via OpenAI."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        try:
            response = self.openai_client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro no OpenAI: {e}")
            return f"[ERRO] Não foi possível conectar à OpenAI: {e}"
