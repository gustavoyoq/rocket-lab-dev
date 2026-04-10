from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.produto import Produto
from app.schemas.produto_schema import ProdutoCreate, ProdutoRead, ProdutoUpdate

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED)
def criar_produto(payload: ProdutoCreate, db: Session = Depends(get_db)):
    produto_existente = db.query(Produto).filter(Produto.id_produto == payload.id_produto).first()

    if produto_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esse produto já existe, tente novamente",
        )

    novo_produto = Produto(
        id_produto=payload.id_produto,
        nome_produto=payload.nome_produto,
        categoria_produto=payload.categoria_produto,
        peso_produto_gramas=payload.peso_produto_gramas,
        comprimento_centimetros=payload.comprimento_centimetros,
        altura_centimetros=payload.altura_centimetros,
        largura_centimetros=payload.largura_centimetros,
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("", response_model=list[ProdutoRead])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return produtos


@router.get("/{id_produto}", response_model=ProdutoRead)
def buscar_produto_por_id(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    return produto


@router.patch("/{id_produto}", response_model=ProdutoRead)
def atualizar_produto(
    id_produto: str,
    payload: ProdutoUpdate,
    db: Session = Depends(get_db),
):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    dados_atualizacao = payload.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizacao.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto


@router.delete("/{id_produto}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    db.delete(produto)
    db.commit()

    return None