from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PedidoBase(BaseModel):
    id_consumidor: str = Field(..., min_length=1, max_length=32)
    status: str = Field(..., min_length=1, max_length=50)
    pedido_compra_timestamp: Optional[datetime] = None
    pedido_entregue_timestamp: Optional[datetime] = None
    data_estimada_entrega: Optional[date] = None
    tempo_entrega_dias: Optional[float] = Field(None, ge=0)
    tempo_entrega_estimado_dias: Optional[float] = Field(None, ge=0)
    diferenca_entrega_dias: Optional[float] = None
    entrega_no_prazo: Optional[str] = Field(None, min_length=1, max_length=10)


class PedidoCreate(PedidoBase):
    id_pedido: str = Field(..., min_length=1, max_length=32)


class PedidoUpdate(BaseModel):
    id_consumidor: Optional[str] = Field(None, min_length=1, max_length=32)
    status: Optional[str] = Field(None, min_length=1, max_length=50)
    pedido_compra_timestamp: Optional[datetime] = None
    pedido_entregue_timestamp: Optional[datetime] = None
    data_estimada_entrega: Optional[date] = None
    tempo_entrega_dias: Optional[float] = Field(None, ge=0)
    tempo_entrega_estimado_dias: Optional[float] = Field(None, ge=0)
    diferenca_entrega_dias: Optional[float] = None
    entrega_no_prazo: Optional[str] = Field(None, min_length=1, max_length=10)


class PedidoRead(PedidoBase):
    id_pedido: str = Field(..., min_length=1, max_length=32)

    model_config = ConfigDict(from_attributes=True)