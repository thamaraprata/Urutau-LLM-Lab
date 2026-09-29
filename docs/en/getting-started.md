# 🚀 Getting Started - EN

## Installation

### Option 1: Docker (recommended)

```bash
# Clone the repository
git clone https://github.com/ThamaraC/urutau-llm-lab.git
cd urutau-llm-lab

# Copy the environment variables
cp .env.example .env

# Bring up the containers
docker compose up -d

# Pull the Ollama model (once, takes ~2min)
docker compose exec ollama ollama pull llama3.1:8b

# Open: http://localhost:5000
```

### Option 2: Local (without Docker)

```bash
# Requirements: Python 3.11+, Ollama installed

# Clone and setup
git clone https://github.com/ThamaraC/urutau-llm-lab.git
cd urutau-llm-lab
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Start Ollama separately
ollama serve
ollama pull llama3.1:8b

# In another terminal, start the app
cp .env.example .env
python app.py

# Open: http://localhost:5000
```

## Usage

1. Open `http://localhost:5000`
2. In the sidebar, pick a challenge
3. Read the challenge briefing
4. Try to exploit the chatbot
5. When you find the "flag", the system lets you know

## Challenge Structure

### ⭐ Challenge 01: Basic Bypass
- **OWASP:** LLM01 - Prompt Injection
- **Goal:** Convince the bot to reveal the master password
- **Hint:** Try roleplay techniques

### ⭐ Challenge 02: System Prompt Leak
- **OWASP:** LLM07 - System Prompt Leakage
- **Goal:** Extract the internal instructions without using keywords
- **Hint:** Try rephrasing the question

### ⭐⭐ Challenge 03: Rogue Agent
- **OWASP:** LLM06 - Excessive Agency
- **Goal:** Force the agent to execute an unauthorized transfer
- **Hint:** Impersonate the admin

### ⭐⭐ Challenge 04: Data Exfiltration
- **OWASP:** LLM02 - Sensitive Information Disclosure
- **Goal:** Leak other customers' PII
- **Hint:** Manipulate the context

### ⭐⭐⭐ Challenge 05: Output Injection
- **OWASP:** LLM05 - Improper Output Handling
- **Goal:** Inject XSS via the LLM's output
- **Hint:** Try different HTML tags

## Instructor Mode

To use it in workshops:

```bash
# 1. Bring up the lab
docker compose up -d

# 2. Explain the challenge (5 min)
# 3. The group tries to exploit it (15 min)
# 4. Show the write-up (5 min)
# 5. Discuss mitigation (5 min)
```

## Troubleshooting

### Ollama won't connect
```bash
# Check whether the container is running
docker compose ps

# Try restarting it
docker compose restart ollama

# Test manually
curl http://localhost:11434/api/version
```

### Model won't download
```bash
# Try manually
docker compose exec ollama ollama pull llama3.1:8b

# Or use a smaller model
# Edit .env: OLLAMA_MODEL=llama3.2:3b
```

### Port 5000 already in use
```bash
# Edit docker-compose.yml
ports:
  - "5001:5000"  # Change to 5001
```

## Next Steps

- Add new challenges (see `contributing.md`)
- Customize the system prompts
- Add your own scoring
- Deploy to a server for remote workshops
