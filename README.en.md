> 🌐 **English** · [Português](README.md)

# 🦉 UrutauLLM-Lab

> A CTF-style lab to learn **LLM Security** hands-on

[![Status](https://img.shields.io/badge/status-nascendo-yellow.svg)](https://github.com/thamaraprata/Urutau-LLM-Lab)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-purple.svg)](https://ollama.com/)
[![OWASP](https://img.shields.io/badge/OWASP-LLM%20Top%2010-red.svg)](https://genai.owasp.org/llm-top-10/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![CI](https://github.com/thamaraprata/Urutau-LLM-Lab/actions/workflows/ci.yml/badge.svg)](https://github.com/thamaraprata/Urutau-LLM-Lab/actions/workflows/ci.yml)
[![Open issues](https://img.shields.io/github/issues/thamaraprata/Urutau-LLM-Lab.svg)](https://github.com/thamaraprata/Urutau-LLM-Lab/issues)
[![Last commit](https://img.shields.io/github/last-commit/thamaraprata/Urutau-LLM-Lab.svg)](https://github.com/thamaraprata/Urutau-LLM-Lab/commits)
[![Repo size](https://img.shields.io/github/repo-size/thamaraprata/Urutau-LLM-Lab.svg)](https://github.com/thamaraprata/Urutau-LLM-Lab)
[![Stars](https://img.shields.io/github/stars/thamaraprata/Urutau-LLM-Lab.svg?style=social)](https://github.com/thamaraprata/Urutau-LLM-Lab/stargazers)

> **⚠️ Project status:** 🚧 Working skeleton, challenges under construction. Check [`ROADMAP.md`](docs/ROADMAP.md) and the [open issues](https://github.com/thamaraprata/Urutau-LLM-Lab/issues) to see what's still missing.

---

## 🎯 What it is

**UrutauLLM-Lab** is an intentionally vulnerable web application, designed to teach security in LLM (Large Language Model) applications through hands-on challenges.

Inspired by projects like **DVWA** and **WebGoat**, but focused on the **OWASP Top 10 for LLM Applications 2025**.

Each challenge is a chatbot with a **planted vulnerability** (prompt injection, system prompt leak, excessive agency, etc). The student interacts with the bot, tries to exploit the flaw, and when they find the "flag" — the system validates it.

---

## 🚧 Current status

| Component | Status | Details |
|------------|--------|----------|
| Flask backend | ✅ Working | REST API with 5 endpoints |
| Frontend | ✅ Working | Dark-themed UI, challenge list, chat |
| Ollama integration | ✅ Working | Local LLM, no cost |
| Docker setup | ✅ Working | `docker compose up` |
| PT-BR documentation | ✅ Complete | README, getting-started, contributing |
| Challenge 01 (Basic Bypass) | ✅ Ready | LLM01: Prompt Injection |
| Challenge 02 (System Prompt Leak) | ✅ Ready | LLM07: System Prompt Leakage |
| Challenge 03 (Rogue Agent) | 🚧 Under construction | LLM06: Excessive Agency |
| Challenge 04 (Data Exfiltration) | ✅ Ready | LLM02: Sensitive Information Disclosure |
| Challenge 05 (Output Injection) | ✅ Ready | LLM05: Improper Output Handling |
| Challenge 06 (Supply Chain) | ✅ Ready | LLM03: Supply Chain |
| Challenges 07-08 | 📋 Planned | LLM09, LLM10 |
| Scoreboard | ✅ Working | SQLite + `/scoreboard`, ranking |
| Auth (session) | ✅ Working | nickname login, `/login` `/logout` |
| Quality metrics | ✅ Working | `/dashboard` + `/api/stats/<id>` |
| Security headers | ✅ Working | CSP, HSTS, X-Frame-Options... |
| API rate limiting | 📋 Planned | Abuse protection |
| Automated tests | ✅ Working | unit + integration (pytest) |
| CI/CD | ✅ Working | GitHub Actions runs pytest |
| EN translation | ✅ Available | this file |

**Check the [open issues](https://github.com/thamaraprata/Urutau-LLM-Lab/issues) to contribute.**

---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- 8GB of available RAM (to run Ollama)
- OR an OpenAI/Anthropic API key

### Option 1: With Ollama (100% local, free)

```bash
git clone https://github.com/thamaraprata/Urutau-LLM-Lab.git
cd urutau-llm-lab
cp .env.example .env
docker compose up -d

# Pull the model (once, takes ~2min)
docker compose exec ollama ollama pull llama3.1:8b

# Open: http://localhost:5000
```

### Option 2: With OpenAI (faster, requires API key)

```bash
git clone https://github.com/thamaraprata/Urutau-LLM-Lab.git
cd urutau-llm-lab
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai docker compose up -d
# Open: http://localhost:5000
```

---

## 🏆 Available challenges

| ID | Name | OWASP LLM | Status | Difficulty |
|----|------|-----------|--------|-------------|
| 00 | Free Chat | — | ✅ Ready | ⭐ |
| 01 | Basic Bypass | LLM01: Prompt Injection | ✅ Ready | ⭐ |
| 02 | System Prompt Leak | LLM07: System Prompt Leakage | ✅ Ready | ⭐ |
| 03 | Rogue Agent | LLM06: Excessive Agency | 🚧 Under construction | ⭐⭐ |
| 04 | Data Exfiltration | LLM02: Sensitive Information Disclosure | ✅ Ready | ⭐⭐ |
| 05 | Output Injection | LLM05: Improper Output Handling | ✅ Ready | ⭐⭐⭐ |
| 06 | Supply Chain Attack | LLM03: Supply Chain | ✅ Ready | ⭐⭐⭐ |
| 07 | Misinformation | LLM09: Misinformation | 📋 Planned | ⭐⭐ |
| 08 | Unbounded Consumption | LLM10: Unbounded Consumption | 📋 Planned | ⭐ |

**Total:** 6 ready (includes Free Chat) + 1 under construction + 2 planned = **9 challenges** covering the OWASP LLM Top 10.

---

## 🤝 How to contribute

**This project is just getting started and community help is very welcome!** 💛

There are many ways to contribute:

### 🐛 Issues to contribute

Issues tagged [`good first issue`](https://github.com/thamaraprata/Urutau-LLM-Lab/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are perfect for anyone just starting out.

Categories:
- 🟢 **good first issue** — easy, great for a first contribution
- 🟡 **help wanted** — needs help
- 🟣 **challenge** — implement a new challenge
- 🔴 **security** — security matter
- 📚 **docs** — documentation

### 💻 Contribute code

```bash
# 1. Fork the project
# 2. Create a branch
git checkout -b feat/meu-challenge

# 3. Implement, add tests
# 4. Commit
git commit -m "feat: adiciona challenge de Data Exfiltration"

# 5. Push and open a PR
git push origin feat/meu-challenge
```

### 📚 Contribute documentation

- Translate the documentation into English
- Improve challenge write-ups
- Add step-by-step tutorials
- Create video lessons (drop the link in the issues)

### 🎨 Contribute design

- Improve the frontend (UX/UI)
- Add animations
- Create a logo/icon
- Responsive theme

### 🧪 Contribute tests

- Add more automated tests
- Improve coverage
- Implement integration tests

### 💡 Contribute ideas

- Ideas for new challenges
- Feedback on the UX
- Architecture suggestions
- Report bugs

**No matter the size of the contribution — every bit of help counts!** 🦉

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│  Frontend: HTML/CSS/JS (Joker theme)    │
│  - Chat UI                               │
│  - Challenge list with status            │
│  - "under construction" banner           │
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
│  - System prompt per challenge          │
│  - Flag detection                        │
└─────────────────────────────────────────┘
```

**Why this stack:**
- **Flask** — simple, easy to read
- **Ollama** — local, free, no API key
- **Plain HTML** — zero build, zero framework
- **SQLite** — zero infra
- **Docker** — `docker compose up` and it runs

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|--------|------------|---------|
| Backend | Python 3.11 + Flask | As simple as possible |
| LLM | Ollama + llama3.1:8b | Local, free, good at PT-BR |
| Frontend | Plain HTML/CSS/JS | Zero build |
| DB | SQLite | Zero infra |
| Container | Docker Compose | Brings everything up with 1 command |
| CI/CD | GitHub Actions | Tests the code on every PR |
| Docs | Markdown | Renders on GitHub |

---

## 🎓 How to use (student mode)

1. Open `http://localhost:5000`
2. Pick a challenge in the sidebar
3. Read the briefing (which vulnerability, context)
4. Try to exploit the chatbot
5. When you find the "flag", the system validates it
6. Read the write-up under "📖 Write-up"

## 🛠️ How to use (instructor mode)

1. Bring up the lab locally
2. Give 15min per challenge
3. The group tries to exploit it together
4. Collective debrief with the write-up
5. Discussion: how do we mitigate?

---

## 📚 References

- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTricks](https://book.hacktricks.xyz/)
- [HackerOne Hacktivity](https://hackerone.com/hacktivity) — real LLM Security reports

---

## 👤 Author

**Thâmara (Dominique) Cordeiro**
- AppSec | AI Security | MLOps | GRC
- Leader of [UrutauSec](https://github.com/thamaraprata) — UFG's Cybersecurity League
- [LinkedIn](https://linkedin.com/in/thamaracordeiro) · [GitHub](https://github.com/thamaraprata)

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

This project was born from a talk at **Amarrando a Portera** (Hub Goiás, 07/18/2026) about "Is your pipeline ready for AI? Adapting CI/CD to the Chaos of MLOps".

Built with 💛, with community help, learning in public.

---

> *"Security is learned by doing, not just by reading."* — Thâmara Cordeiro
