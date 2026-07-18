# 🤝 Como Contribuir

> 🚧 **Esse projeto tá nascendo agora e a ajuda da comunidade é fundamental!**

Quer adicionar um challenge? Melhorar a documentação? Reportar um bug? Bora!

## 🌟 Bem-vindos

Esse é um projeto **open source** criado com 3 princípios:
1. **Aprender fazendo** — a melhor forma de aprender segurança é construindo
2. **Construir aberto** — em público, vulnerável, com erros
3. **Comunidade primeiro** — toda ajuda vale, do PR ao feedback

Não importa seu nível. Tem issues pra todo mundo.

## 🏷️ Labels que usamos

- 🟢 **`good first issue`** — fácil, perfeito pra primeira contribuição
- 🟡 **`help wanted`** — precisa de ajuda
- 🟣 **`challenge`** — implementar novo challenge
- 🔴 **`security`** — questão de segurança
- 📚 **`docs`** — documentação
- 🛠️ **`enhancement`** — melhoria de feature
- 🧪 **`tests`** — testes

## 🚀 Primeiros passos

### 1. Setup local
```bash
git clone https://github.com/thamaraprata/Urutau-LLM-Lab.git
cd urutau-llm-lab
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d
```

### 2. Rode os testes
```bash
python tests/test_challenges.py
```

### 3. Escolha uma issue
- Veja as [issues abertas](https://github.com/thamaraprata/Urutau-LLM-Lab/issues)
- Comece pelas `good first issue` se for novo
- Comente na issue que você vai pegar

### 4. Faça um fork e crie uma branch
```bash
# No GitHub: clique em "Fork"
git clone https://github.com/SEU-USER/Urutau-LLM-Lab.git
cd urutau-LLM-Lab
git checkout -b feat/seu-feature-aqui
```

### 5. Implemente e teste
```bash
# Implementa
# Adiciona testes
python tests/test_challenges.py

# Verifica lint
flake8 .
```

### 6. Commit e push
```bash
git add .
git commit -m "feat: descrição clara do que mudou"
git push origin feat/seu-feature-aqui
```

### 7. Abra um Pull Request
- No GitHub, clique em "New Pull Request"
- Descreva o que mudou e por quê
- Referencie a issue (ex: "Closes #4")

## 🎯 Adicionando um Challenge

### 1. Escolha uma categoria do OWASP LLM Top 10

Veja: https://genai.owasp.org/llm-top-10/

### 2. Edite `llm/challenges.py`

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

### 3. Teste localmente
```bash
python tests/test_challenges.py
docker compose restart app
```

### 4. Valide a flag manualmente
- Acesse http://localhost:5000
- Tente 3+ payloads diferentes
- Todos devem revelar a flag
- O sistema deve marcar como `flag_found: true`

### 5. Faça um PR

## 📋 Guidelines

### System Prompts
- **Realista** — deve parecer um app em produção
- **Focado** — 1 vulnerabilidade principal por challenge
- **Educativo** — o write-up deve ensinar a mitigar

### Flags
- **Únicas** — cada challenge tem sua flag
- **Fáceis de validar** — string simples, case-insensitive
- **Não óbvias** — usuário precisa pensar um pouco

### Write-ups
- **Solução** — 2-3 payloads que funcionam
- **Mitigação** — como proteger em produção
- **OWASP** — referência à categoria
- **Links** — para recursos externos quando relevante

## 📚 Tipos de contribuição

### 💻 Código
- Novos challenges
- Features (scoreboard, auth, etc)
- Bug fixes
- Performance

### 📚 Documentação
- Tradução pra inglês
- Tutoriais passo-a-passo
- Comentários no código
- Melhoria do README

### 🎨 Design
- Logo do projeto
- Melhorias no frontend
- Temas
- Acessibilidade

### 🧪 Testes
- Testes unitários
- Testes de integração
- Cobertura
- CI/CD

### 💡 Ideias
- Sugestões de challenges
- Feedback de UX
- Reportar bugs
- Discutir arquitetura

## 🌐 Comunicação

- **GitHub Issues** — bugs, features, dúvidas
- **GitHub Discussions** — ideias, perguntas gerais
- **LinkedIn** — DM pra autora

## 📜 Code of Conduct

- Seja respeitoso
- Não exponha vulnerabilidades reais
- Use apenas em ambientes controlados
- Eduque, não humilhe
- Lembre-se: todo mundo foi iniciante um dia

## 🙏 Agradecimentos

Toda contribuição, do PR mais complexo ao typo fix, é valiosa. Obrigada por ajudar a construir isso! 🦉

---

> *"Segurança se aprende fazendo, não só lendo."*
