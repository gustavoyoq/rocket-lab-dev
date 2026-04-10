from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AvaliacaoPedidoBase(BaseModel):
    id_pedido: str = Field(..., min_length=1, max_length=32)
    avaliacao: int = Field(..., ge=1, le=5)
    titulo_comentario: Optional[str] = Field(None, min_length=1, max_length=255)
    comentario: Optional[str] = Field(None, min_length=1, max_length=1000)
    data_comentario: Optional[datetime] = None
    data_resposta: Optional[datetime] = None


class AvaliacaoPedidoCreate(AvaliacaoPedidoBase):
    id_avaliacao: str = Field(..., min_length=1, max_length=32)


class AvaliacaoPedidoUpdate(BaseModel):
    id_pedido: Optional[str] = Field(None, min_length=1, max_length=32)
    avaliacao: Optional[int] = Field(None, ge=1, le=5)
    titulo_comentario: Optional[str] = Field(None, min_length=1, max_length=255)
    comentario: Optional[str] = Field(None, min_length=1, max_length=1000)
    data_comentario: Optional[datetime] = None
    data_resposta: Optional[datetime] = None


class AvaliacaoPedidoRead(AvaliacaoPedidoBase):
    id_avaliacao: str = Field(..., min_length=1, max_length=32)

    model_config = ConfigDict(from_attributes=True)