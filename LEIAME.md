# Avaliação — Arquitetura de Software (Aulas 8 e 9)

| Pasta | Prática |
|---|---|
| `api_simples/` | Aula 8 · Prática 1 — API FastAPI em contêiner |
| `mysql_container/` | Aula 8 · Prática 2 — MySQL com volume |
| `api_mysql/` | Aula 8 · Prática 3 — API + MySQL com Docker Compose |
| `microsservicos_mq/` | Aula 9 · Práticas 1 e 2 — Pedidos + RabbitMQ + CI (GitHub Actions) |

## Como executar
```bash
# Prática 1
cd api_simples && docker build -t api-tarefas:1.0 . && docker run -d --name api-tarefas -p 8000:8000 api-tarefas:1.0

# Prática 2
bash mysql_container/executar_mysql.sh

# Prática 3
cd api_mysql && cp .env.example .env && docker compose up -d --build

# Aula 9 (Práticas 1 e 2)
cd microsservicos_mq && cp .env.example .env && docker compose up -d --build
cd pedidos_api && pip install -r requirements.txt -r requirements-dev.txt && pytest -q
```
Nunca envie o arquivo `.env` ao GitHub (já está no `.gitignore`).
