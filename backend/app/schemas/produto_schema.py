from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProdutoBase(BaseModel):

    nome_produto: str = Field(..., min_length=1, max_length=255)
    categoria_produto: str = Field(..., min_length=1, max_length=100)
    imagem_url: Optional[str] = Field(None, min_length=1, max_length=2048)
    peso_produto_gramas: Optional[float] = Field(None, ge=0)
    comprimento_centimetros: Optional[float] = Field(None, ge=0)
    altura_centimetros: Optional[float] = Field(None, ge=0)
    largura_centimetros: Optional[float] = Field(None, ge=0)


class ProdutoCreate(ProdutoBase):
    id_produto: str = Field(..., min_length=1, max_length=32)


class ProdutoUpdate(BaseModel):
    nome_produto: Optional[str] = Field(None, min_length=1, max_length=255)
    categoria_produto: Optional[str] = Field(None, min_length=1, max_length=100)
    imagem_url: Optional[str] = Field(None, min_length=1, max_length=2048)
    peso_produto_gramas: Optional[float] = Field(None, ge=0)
    comprimento_centimetros: Optional[float] = Field(None, ge=0)
    altura_centimetros: Optional[float] = Field(None, ge=0)
    largura_centimetros: Optional[float] = Field(None, ge=0)


class ProdutoRead(ProdutoBase):
    id_produto: str = Field(..., min_length=1, max_length=32)

    model_config = ConfigDict(from_attributes=True)