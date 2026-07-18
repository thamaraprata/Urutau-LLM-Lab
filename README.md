# 🦉 UrutauLLM-Lab

> Laboratório CTF-style para aprender **LLM Security** na prática

[![Status](https://img.shields.io/badge/status-nascendo-yellow.svg)](https://github.com/thamaraprata/Urutau-LLM-Lab)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-purple.svg)](https://ollama.com/)
[![OWASP](https://img.shields.io/badge/OWASP-LLM%20Top%2010-red.svg)](https://genai.owasp.org/llm-top-10/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> **⚠️ Status do projeto:** 🚧 Esqueleto funcional, challenges em construção. Veja [`ROADMAP.md`](docs/ROADMAP.md) e [issues abertas](https://github.com/thamaraprata/Urutau-LLM-Lab/issues) para saber o que falta.

---

## 🎯 O que é

**UrutauLLM-Lab** é uma aplicação web intencionalmente vulnerável, projetada para ensinar segurança em aplicações LLM (Large Language Models) através de desafios hands-on.

Inspirado em projetos como **DVWA** e **WebGoat**, mas focado no **OWASP Top 10 for LLM Applications 2025**.

Cada challenge é um chatbot com uma **vulnerabilidade plantada** (prompt injection, system prompt leak, excessive agency, etc). O aluno interage com o bot, tenta explorar a falha, e quando encontra a "flag" — o sistema valida.

---

## 🚧 Status atual

| Componente | Status | Detalhes |
|------------|--------|----------|
| Backend Flask | ✅ Funcional | API REST com 5 endpoints |
| Frontend | ✅ Funcional | UI com tema escuro, lista de challenges, chat |
| Integração Ollama | ✅ Funcional | LLM local, sem custo |
| Docker setup | ✅ Funcional | `docker compose up` |
| Documentação PT-BR | ✅ Completa | README, getting-started, contributing |
| Challenge 01 (Bypass Básico) | ✅ Pronto | LLM01: Prompt Injection |
| Challenge 02 (Vazamento SP) | ✅ Pronto | LLM07: System Prompt Leakage |
| Challenge 03 (Agente Rebelde) | 🚧 Em construção | LLM06: Excessive Agency |
| Challenges 04-08 | 📋 Planejados | LLM02, LLM05, LLM03, LLM09, LLM10 |
| Scoreboard | 📋 Planejado | Persistência de progresso |
| API rate limiting | 📋 Planejado | Proteção contra abuse |
| Testes automatizados | 🚧 Parcial | test_challenges.py |
| CI/CD | 📋 Planejado | GitHub Actions melhorado |
| Tradução EN | 📋 Planejado | Welcome contributors! |

**Veja as [issues abertas](https://github.com/thamaraprata/Urutau-LLM-Lab/issues) para contribuir.**

---

## 🚀 Quick Start

### Pré-requisitos

- Docker e Docker Compose
- 8GB de RAM disponível (pra rodar o Ollama)
- OU uma API key da OpenAI/Anthropic

### Opção 1: Com Ollama (100% local, grátis)

```bash
git clone https://github.com/thamaraprata/Urutau-LLM-Lab.git
cd urutau-llm-lab
cp .env.example .env
docker compose up -d

# Baixa o modelo (1x, demora ~2min)
docker compose exec ollama ollama pull llama3.1:8b

# Acesse: http://localhost:5000
```

### Opção 2: Com OpenAI (mais rápido, requer API key)

```bash
git clone https://github.com/thamaraprata/Urutau-LLM-Lab.git
cd urutau-llm-lab
cp .env.example .env
# Edite .env e adicione: OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai docker compose up -d
# Acesse: http://localhost:5000
```

---

## 🏆 Challenges disponíveis

| ID | Nome | OWASP LLM | Status | Dificuldade |
|----|------|-----------|--------|-------------|
| 00 | Chat Livre | — | ✅ Pronto | ⭐ |
| 01 | Bypass Básico | LLM01: Prompt Injection | ✅ Pronto | ⭐ |
| 02 | Vazamento de System Prompt | LLM07: System Prompt Leakage | ✅ Pronto | ⭐ |
| 03 | Agente Rebelde | LLM06: Excessive Agency | 🚧 Em construção | ⭐⭐ |
| 04 | Data Exfiltration | LLM02: Sensitive Information Disclosure | 📋 Planejado | ⭐⭐ |
| 05 | Output Injection | LLM05: Improper Output Handling | 📋 Planejado | ⭐⭐⭐ |
| 06 | Supply Chain Attack | LLM03: Supply Chain | 📋 Planejado | ⭐⭐⭐ |
| 07 | Misinformation | LLM09: Misinformation | 📋 Planejado | ⭐⭐ |
| 08 | Unbounded Consumption | LLM10: Unbounded Consumption | 📋 Planejado | ⭐ |

**Total:** 2 prontos + 1 em construção + 6 planejados = **9 challenges planejados** cobrindo o OWASP LLM Top 10.

---

## 🤝 Como contribuir

**Esse projeto tá nascendo agora e a ajuda da comunidade é bem-vinda!** 💛

Tem várias formas de contribuir:

### 🐛 Issues pra contribuir

Issues marcadas com [`good first issue`](https://github.com/thamaraprata/Urutau-LLM-Lab/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) são perfeitas pra quem tá começando.

Categorias:
- 🟢 **good first issue** — fácil, bom pra primeira contribuição
- 🟡 **help wanted** — precisa de ajuda
- 🟣 **challenge** — implementar um novo challenge
- 🔴 **security** — questão de segurança
- 📚 **docs** — documentação

### 💻 Contribuir com código

```bash
# 1. Fork o projeto
# 2. Crie uma branch
git checkout -b feat/meu-challenge

# 3. Implemente, adicione testes
# 4. Commit
git commit -m "feat: adiciona challenge de Data Exfiltration"

# 5. Push e abra PR
git push origin feat/meu-challenge
```

### 📚 Contribuir com documentação

- Traduzir a documentação pra inglês
- Melhorar write-ups de challenges
- Adicionar tutoriais passo-a-passo
- Criar vídeo-aulas (manda link nos issues)

### 🎨 Contribuir com design

- Melhorar o frontend (UX/UI)
- Adicionar animações
- Criar logo/ícone
- Tema responsivo

### 🧪 Contribuir com testes

- Adicionar mais testes automatizados
- Melhorar cobertura
- Implementar testes de integração

### 💡 Contribuir com ideias

- Ideias de novos challenges
- Feedback sobre a UX
- Sugestões de arquitetura
- Reportar bugs

**Não importa o tamanho da contribuição — toda ajuda vale!** 🦉

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│  Frontend: HTML/CSS/JS (tema Joker)     │
│  - Chat UI                               │
│  - Lista de challenges com status        │
│  - Banner "em construção"                │
└─────────────┬───────────────────────────┘
              ↓ HTTP
┌─────────────────────────────────────────┐
│  Backend: Python + Flask                │
│  - /api/chat                             │
│  - /api/challenges                       │
│  - /api/challenges/<id>/hint             │
│  - /api/challenges/<id>/writeup          │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  LLM Provider (Ollama / OpenAI)         │
│  - System prompt por challenge          │
│  - Detecção de flag                      │
└─────────────────────────────────────────┘
```

**Por que essa stack:**
- **Flask** — simples, fácil de ler
- **Ollama** — local, grátis, sem API key
- **HTML puro** — zero build, zero framework
- **SQLite** — zero infra
- **Docker** — `docker compose up` e roda

---

## 🛠️ Stack Técnico

| Camada | Tecnologia | Por que |
|--------|------------|---------|
| Backend | Python 3.11 + Flask | Mais simples possível |
| LLM | Ollama + llama3.1:8b | Local, grátis, bom em PT-BR |
| Frontend | HTML/CSS/JS puro | Zero build |
| DB | SQLite | Zero infra |
| Container | Docker Compose | Sobe tudo com 1 comando |
| CI/CD | GitHub Actions | Testa código a cada PR |
| Docs | Markdown | Renderiza no GitHub |

---

## 🎓 Como usar (modo aluno)

1. Acesse `http://localhost:5000`
2. Escolha um challenge na sidebar
3. Leia o briefing (qual vulnerabilidade, contexto)
4. Tente explorar o chatbot
5. Quando achar a "flag", o sistema valida
6. Veja o write-up em "📖 Write-up"

## 🛠️ Como usar (modo professor)

1. Sobe o lab localmente
2. Dá 15min pra cada challenge
3. Galera tenta explorar em grupo
4. Debriefing coletivo com o write-up
5. Discussão: como mitigar?

---

## 📚 Referências

- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTricks](https://book.hacktricks.xyz/)
- [HackerOne Hacktivity](https://hackerone.com/hacktivity) — reports reais de LLM Security

---

## 👤 Autora

**Thâmara (Dominique) Cordeiro**
- AppSec | IA Security | MLOps | GRC
- Líder da [UrutauSec](https://github.com/thamaraprata) — Liga de Cibersegurança da UFG
- [LinkedIn](https://linkedin.com/in/thamaracordeiro) · [GitHub](https://github.com/thamaraprata)

---

## 📜 Licença

MIT License — veja [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

Esse projeto nasceu de uma palestra no **Amarrando a Portera** (Hub Goiás, 18/07/2026) sobre "Seu Pipeline está pronto para IA? Adaptando a CI/CD para o Caos do MLOps".

Construído com 💛, com ajuda da comunidade, aprendendo em público.

---

> *"Segurança se aprende fazendo, não só lendo."* — Thâmara Cordeiro
