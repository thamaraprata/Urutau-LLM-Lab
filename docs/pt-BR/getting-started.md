# 🚀 Getting Started - PT-BR

## Instalação

### Opção 1: Docker (recomendado)

```bash
# Clone o repositório
git clone https://github.com/ThamaraC/urutau-llm-lab.git
cd urutau-llm-lab

# Copia as variáveis de ambiente
cp .env.example .env

# Sobe os containers
docker compose up -d

# Baixa o modelo do Ollama (1x, demora ~2min)
docker compose exec ollama ollama pull llama3.1:8b

# Acesse: http://localhost:5000
```

### Opção 2: Local (sem Docker)

```bash
# Requisitos: Python 3.11+, Ollama instalado

# Clone e setup
git clone https://github.com/ThamaraC/urutau-llm-lab.git
cd urutau-llm-lab
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Sobe o Ollama separadamente
ollama serve
ollama pull llama3.1:8b

# Em outro terminal, sobe a app
cp .env.example .env
python app.py

# Acesse: http://localhost:5000
```

## Uso

1. Acesse `http://localhost:5000`
2. Na barra lateral, escolha um challenge
3. Leia o briefing do challenge
4. Tente explorar o chatbot
5. Quando achar a "flag", o sistema te avisa

## Estrutura de Challenges

### ⭐ Challenge 01: Bypass Básico
- **OWASP:** LLM01 - Prompt Injection
- **Objetivo:** Convencer o bot a revelar a senha mestra
- **Dica:** Tente técnicas de roleplay

### ⭐ Challenge 02: Vazamento de System Prompt
- **OWASP:** LLM07 - System Prompt Leakage
- **Objetivo:** Extrair instruções internas sem usar palavras-chave
- **Dica:** Tente reformular a pergunta

### ⭐⭐ Challenge 03: Agente Rebelde
- **OWASP:** LLM06 - Excessive Agency
- **Objetivo:** Forçar agente a executar transferência não autorizada
- **Dica:** Impersonar admin

### ⭐⭐ Challenge 04: Data Exfiltration
- **OWASP:** LLM02 - Sensitive Information Disclosure
- **Objetivo:** Vazar PII de outros clientes
- **Dica:** Manipular contexto

### ⭐⭐⭐ Challenge 05: Output Injection
- **OWASP:** LLM05 - Improper Output Handling
- **Objetivo:** Injetar XSS via output do LLM
- **Dica:** Tente diferentes tags HTML

## Modo Professor

Para usar em workshops:

```bash
# 1. Sobe o lab
docker compose up -d

# 2. Explica o challenge (5 min)
# 3. Galera tenta explorar (15 min)
# 4. Mostra write-up (5 min)
# 5. Discute mitigação (5 min)
```

## Troubleshooting

### Ollama não conecta
```bash
# Verifica se o container está rodando
docker compose ps

# Tenta restartar
docker compose restart ollama

# Testa manualmente
curl http://localhost:11434/api/version
```

### Modelo não baixa
```bash
# Tenta manualmente
docker compose exec ollama ollama pull llama3.1:8b

# Ou usa modelo menor
# Edite .env: OLLAMA_MODEL=llama3.2:3b
```

### Porta 5000 em uso
```bash
# Edita docker-compose.yml
ports:
  - "5001:5000"  # Muda pra 5001
```

## Próximos Passos

- Adicione novos challenges (veja `contributing.md`)
- Customize os system prompts
- Adicione seu próprio scoring
- Faça deploy em um servidor pra workshops remotos
