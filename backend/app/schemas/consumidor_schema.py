from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ConsumidorBase(BaseModel):
    prefixo_cep: str = Field(..., min_length=1, max_length=10)
    nome_consumidor: str = Field(..., min_length=1, max_length=255)
    cidade: str = Field(..., min_length=1, max_length=100)
    estado: str = Field(..., min_length=2, max_length=2)


class ConsumidorCreate(ConsumidorBase):
    id_consumidor: str = Field(..., min_length=1, max_length=32)


class ConsumidorUpdate(BaseModel):
    prefixo_cep: Optional[str] = Field(None, min_length=1, max_length=10)
    nome_consumidor: Optional[str] = Field(None, min_length=1, max_length=255)
    cidade: Optional[str] = Field(None, min_length=1, max_length=100)
    estado: Optional[str] = Field(None, min_length=2, max_length=2)


class ConsumidorRead(ConsumidorBase):
    id_consumidor: str = Field(..., min_length=1, max_length=32)

    model_config = ConfigDict(from_attributes=True)