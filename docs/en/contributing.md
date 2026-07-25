# 🤝 How to Contribute

> 🚧 **This project is just getting started and community help is essential!**

Want to add a challenge? Improve the documentation? Report a bug? Let's go!

## 🌟 Welcome

This is an **open source** project built on 3 principles:
1. **Learn by doing** — the best way to learn security is by building
2. **Build in the open** — in public, vulnerable, with mistakes
3. **Community first** — every bit of help counts, from a PR to feedback

Your level doesn't matter. There are issues for everyone.

## 🏷️ Labels we use

- 🟢 **`good first issue`** — easy, perfect for a first contribution
- 🟡 **`help wanted`** — needs help
- 🟣 **`challenge`** — implement a new challenge
- 🔴 **`security`** — security matter
- 📚 **`docs`** — documentation
- 🛠️ **`enhancement`** — feature improvement
- 🧪 **`tests`** — tests

## 🚀 First steps

### 1. Local setup
```bash
git clone https://github.com/thamaraprata/Urutau-LLM-Lab.git
cd urutau-llm-lab
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d
```

### 2. Run the tests
```bash
python tests/test_challenges.py
```

### 3. Pick an issue
- Check the [open issues](https://github.com/thamaraprata/Urutau-LLM-Lab/issues)
- Start with the `good first issue` ones if you're new
- Comment on the issue to say you're taking it

### 4. Fork and create a branch
```bash
# On GitHub: click "Fork"
git clone https://github.com/SEU-USER/Urutau-LLM-Lab.git
cd urutau-LLM-Lab
git checkout -b feat/seu-feature-aqui
```

### 5. Implement and test
```bash
# Implement
# Add tests
python tests/test_challenges.py

# Check lint
flake8 .
```

### 6. Commit and push
```bash
git add .
git commit -m "feat: descrição clara do que mudou"
git push origin feat/seu-feature-aqui
```

### 7. Open a Pull Request
- On GitHub, click "New Pull Request"
- Describe what changed and why
- Reference the issue (e.g. "Closes #4")

## 🎯 Adding a Challenge

### 1. Pick a category from the OWASP LLM Top 10

See: https://genai.owasp.org/llm-top-10/

### 2. Edit `llm/challenges.py`

```python
"09": {
    "id": "09",
    "name": "Seu Challenge Aqui",
    "owasp": "LLM08: Vector and Embedding Weaknesses",
    "difficulty": "⭐⭐",
    "status": "ready",  # ou "wip" ou "planned"
    "description": "Descrição clara do objetivo...",
    "system_prompt": "O system prompt vulnerável...",
    "hint": "Dica de como resolver",
    "writeup": "Solução completa + mitigações",
    "flag_pattern": "FLAG-QUE-USUARIO-PRECISA-ENCONTRAR",
},
```

### 3. Test locally
```bash
python tests/test_challenges.py
docker compose restart app
```

### 4. Validate the flag manually
- Open http://localhost:5000
- Try 3+ different payloads
- They should all reveal the flag
- The system should mark it as `flag_found: true`

### 5. Open a PR

## 📋 Guidelines

### System Prompts
- **Realistic** — it should look like a production app
- **Focused** — 1 main vulnerability per challenge
- **Educational** — the write-up should teach how to mitigate

### Flags
- **Unique** — each challenge has its own flag
- **Easy to validate** — a simple, case-insensitive string
- **Not obvious** — the user needs to think a bit

### Write-ups
- **Solution** — 2-3 payloads that work
- **Mitigation** — how to protect against it in production
- **OWASP** — reference to the category
- **Links** — to external resources when relevant

## 📚 Types of contribution

### 💻 Code
- New challenges
- Features (scoreboard, auth, etc)
- Bug fixes
- Performance

### 📚 Documentation
- Translation into English
- Step-by-step tutorials
- Comments in the code
- README improvements

### 🎨 Design
- Project logo
- Frontend improvements
- Themes
- Accessibility

### 🧪 Tests
- Unit tests
- Integration tests
- Coverage
- CI/CD

### 💡 Ideas
- Challenge suggestions
- UX feedback
- Report bugs
- Discuss architecture

## 🌐 Communication

- **GitHub Issues** — bugs, features, questions
- **GitHub Discussions** — ideas, general questions
- **LinkedIn** — DM the author

## 📜 Code of Conduct

- Be respectful
- Don't expose real vulnerabilities
- Use it only in controlled environments
- Educate, don't humiliate
- Remember: everyone was a beginner once

## 🙏 Acknowledgments

Every contribution, from the most complex PR to a typo fix, is valuable. Thank you for helping build this! 🦉

---

> *"Security is learned by doing, not just by reading."*
