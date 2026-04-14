from datetime import datetime
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
    categoria_produto: str = Field(..., min_length=0, max_length=100)

    model_config = ConfigDict(from_attributes=True)


class ProdutoListItemRead(ProdutoRead):
    sales_count: int = Field(..., ge=0)
    average_rating: float = Field(..., ge=0)
    review_count: int = Field(..., ge=0)


class ProdutoPaginatedRead(BaseModel):
    items: list[ProdutoListItemRead]
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1)
    total_items: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=1)


class ProdutoDetalhesRead(ProdutoRead):
    sales_count: int = Field(..., ge=0)
    average_rating: float = Field(..., ge=0)
    review_count: int = Field(..., ge=0)
    estimated_price_brl: Optional[float] = Field(None, ge=0)


class ProdutoAvaliacaoItemRead(BaseModel):
    id_avaliacao: str = Field(..., min_length=1, max_length=32)
    id_pedido: str = Field(..., min_length=1, max_length=32)
    avaliacao: int = Field(..., ge=1, le=5)
    titulo_comentario: Optional[str] = Field(None, min_length=1, max_length=255)
    comentario: Optional[str] = Field(None, min_length=1, max_length=1000)
    data_comentario: Optional[datetime] = None
    data_resposta: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProdutoAvaliacoesPaginatedRead(BaseModel):
    items: list[ProdutoAvaliacaoItemRead]
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1)
    total_items: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=1)