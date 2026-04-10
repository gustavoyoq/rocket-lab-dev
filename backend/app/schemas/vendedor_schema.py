from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VendedorBase(BaseModel):
    nome_vendedor: str = Field(..., min_length=1, max_length=255)
    prefixo_cep: str = Field(..., min_length=1, max_length=10)
    cidade: str = Field(..., min_length=1, max_length=100)
    estado: str = Field(..., min_length=2, max_length=2)


class VendedorCreate(VendedorBase):
    id_vendedor: str = Field(..., min_length=1, max_length=32)


class VendedorUpdate(BaseModel):
    nome_vendedor: Optional[str] = Field(None, min_length=1, max_length=255)
    prefixo_cep: Optional[str] = Field(None, min_length=1, max_length=10)
    cidade: Optional[str] = Field(None, min_length=1, max_length=100)
    estado: Optional[str] = Field(None, min_length=2, max_length=2)


class VendedorRead(VendedorBase):
    id_vendedor: str = Field(..., min_length=1, max_length=32)

    model_config = ConfigDict(from_attributes=True)