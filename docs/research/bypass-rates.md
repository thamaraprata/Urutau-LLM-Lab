# Bypass-rate por modelo LLM (#10)

**Challenge:** 01 — Bypass Básico (LLM01: Prompt Injection)
**Payloads:** 8 · **Flag:** `PWNED-2024`

> ⚠️ **TEMPLATE — dry run.** Nenhum modelo foi consultado. Rode o harness com Ollama vivo para preencher os números reais.

| Modelo | Tentativas | Bypasses | Taxa de bypass | Robustez |
|---|---|---|---|---|
| `llama3.1:8b` | 0 | 0 | 0.0% | — |
| `llama3.2:3b` | 0 | 0 | 0.0% | — |
| `mistral:7b` | 0 | 0 | 0.0% | — |

**Leitura:** menor taxa de bypass = guardrail mais robusto. Para produção, prefira o modelo com menor bypass no seu conjunto de ataques representativo — mas nunca confie só no modelo: defesa em camadas (validação de input, hardening do system prompt, filtros de saída, human-in-the-loop) continua obrigatória.

_Metodologia: `docs/research/bypass-benchmark.md`. Gerado por `research/bypass_benchmark.py`._
