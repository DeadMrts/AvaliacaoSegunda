FROM python:3.14-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd --create-home appuser
USER appuser

# -u: saída sem buffer, para os logs aparecerem em tempo real no docker logs.
CMD ["python", "-u", "app/worker.py"]
