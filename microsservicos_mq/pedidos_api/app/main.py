"""Serviço de pedidos: recebe o pedido por HTTP e publica o evento pedido.criado no RabbitMQ."""
import json
import os
import uuid
from datetime import datetime, timezone

import pika
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

FILA = "pedido.criado"

app = FastAPI(title="Pedidos API", version="1.0.0")


class PedidoEntrada(BaseModel):
    cliente: str = Field(min_length=3, max_length=100)
    valor_total: float = Field(gt=0)


class PedidoRecebido(BaseModel):
    id: str
    status: str


class PublicadorRabbit:
    """Publica eventos na fila. Abre uma conexão por mensagem: simples e robusto para a aula."""

    def __init__(self, url: str):
        self._params = pika.URLParameters(url)

    def publicar(self, evento: dict) -> None:
        with pika.BlockingConnection(self._params) as con:
            canal = con.channel()
            canal.queue_declare(queue=FILA, durable=True)  # a fila sobrevive a reinício do broker
            canal.basic_publish(
                exchange="",  # exchange padrão: roteia pelo nome da fila
                routing_key=FILA,
                body=json.dumps(evento).encode(),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=pika.DeliveryMode.Persistent,  # mensagem gravada em disco
                    message_id=evento["id"],
                ),
            )


def obter_publicador() -> PublicadorRabbit:
    return PublicadorRabbit(os.environ.get("AMQP_URL", "amqp://guest:guest@localhost:5672/"))


@app.get("/saude")
def saude():
    return {"api": "ok"}


@app.post("/pedidos", response_model=PedidoRecebido, status_code=status.HTTP_202_ACCEPTED)
def criar_pedido(entrada: PedidoEntrada, publicador: PublicadorRabbit = Depends(obter_publicador)):
    evento = {
        "id": str(uuid.uuid4()),
        "cliente": entrada.cliente,
        "valor_total": entrada.valor_total,
        "criado_em": datetime.now(timezone.utc).isoformat(),
    }
    try:
        publicador.publicar(evento)
    except pika.exceptions.AMQPError:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Broker de mensagens indisponível")
    # 202 Accepted: o pedido foi aceito; a notificação será processada de forma assíncrona.
    return {"id": evento["id"], "status": "RECEBIDO"}
