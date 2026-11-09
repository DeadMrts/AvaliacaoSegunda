# Imagem base oficial, variante slim (menor superfície e tamanho).
FROM python:3.14-slim

WORKDIR /code

# requirements antes do código: a camada de dependências fica em cache
# enquanto o requirements.txt não mudar.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Executa sem privilégios de root.
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Forma exec (lista JSON): o processo recebe SIGTERM e encerra de forma limpa.
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
