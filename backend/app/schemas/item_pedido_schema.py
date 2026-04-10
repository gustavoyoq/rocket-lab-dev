from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemPedidoBase(BaseModel):
    id_produto: str = Field(..., min_length=1, max_length=32)
    id_vendedor: str = Field(..., min_length=1, max_length=32)
    preco_BRL: float = Field(..., ge=0)
    preco_frete: float = Field(..., ge=0)


class ItemPedidoCreate(ItemPedidoBase):
    id_pedido: str = Field(..., min_length=1, max_length=32)
    id_item: int = Field(..., ge=1)


class ItemPedidoUpdate(BaseModel):
    id_produto: Optional[str] = Field(None, min_length=1, max_length=32)
    id_vendedor: Optional[str] = Field(None, min_length=1, max_length=32)
    preco_BRL: Optional[float] = Field(None, ge=0)
    preco_frete: Optional[float] = Field(None, ge=0)


class ItemPedidoRead(ItemPedidoBase):
    id_pedido: str = Field(..., min_length=1, max_length=32)
    id_item: int = Field(..., ge=1)

    model_config = ConfigDict(from_attributes=True)