from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.models.item_pedido import ItemPedido
from app.models.produto import Produto
from app.schemas.produto_schema import (
    ProdutoAvaliacoesPaginatedRead,
    ProdutoCreate,
    ProdutoDetalhesRead,
    ProdutoPaginatedRead,
    ProdutoRead,
    ProdutoUpdate,
)

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
        imagem_url=payload.imagem_url,
        peso_produto_gramas=payload.peso_produto_gramas,
        comprimento_centimetros=payload.comprimento_centimetros,
        altura_centimetros=payload.altura_centimetros,
        largura_centimetros=payload.largura_centimetros,
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("", response_model=ProdutoPaginatedRead)
def listar_produtos(
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=100),
    search: str | None = Query(None),
    categoria: str | None = Query(None),
    db: Session = Depends(get_db),
):
    sales_subquery = (
        db.query(
            ItemPedido.id_produto.label("id_produto"),
            func.count(ItemPedido.id_item).label("sales_count"),
        )
        .group_by(ItemPedido.id_produto)
        .subquery()
    )

    reviews_subquery = (
        db.query(
            ItemPedido.id_produto.label("id_produto"),
            func.avg(AvaliacaoPedido.avaliacao).label("average_rating"),
            func.count(AvaliacaoPedido.id_avaliacao).label("review_count"),
        )
        .join(AvaliacaoPedido, AvaliacaoPedido.id_pedido == ItemPedido.id_pedido)
        .group_by(ItemPedido.id_produto)
        .subquery()
    )

    filters = []

    normalized_search = (search or "").strip().lower()
    if normalized_search:
        search_pattern = f"%{normalized_search}%"
        filters.append(
            or_(
                func.lower(Produto.id_produto).like(search_pattern),
                func.lower(Produto.nome_produto).like(search_pattern),
                func.lower(Produto.categoria_produto).like(search_pattern),
            )
        )

    normalized_category = (categoria or "").strip().lower()
    if normalized_category and normalized_category != "all":
        filters.append(func.lower(Produto.categoria_produto) == normalized_category)

    total_items_query = db.query(func.count(Produto.id_produto))
    if filters:
        total_items_query = total_items_query.filter(*filters)

    total_items = total_items_query.scalar() or 0
    total_pages = max(1, ceil(total_items / page_size))

    if page > total_pages:
        page = total_pages

    paged_query = (
        db.query(
            Produto,
            func.coalesce(sales_subquery.c.sales_count, 0).label("sales_count"),
            func.coalesce(reviews_subquery.c.average_rating, 0.0).label("average_rating"),
            func.coalesce(reviews_subquery.c.review_count, 0).label("review_count"),
        )
        .outerjoin(sales_subquery, sales_subquery.c.id_produto == Produto.id_produto)
        .outerjoin(reviews_subquery, reviews_subquery.c.id_produto == Produto.id_produto)
    )

    if filters:
        paged_query = paged_query.filter(*filters)

    rows = paged_query.offset((page - 1) * page_size).limit(page_size).all()

    items = [
        {
            "id_produto": produto.id_produto,
            "nome_produto": produto.nome_produto,
            "categoria_produto": produto.categoria_produto,
            "imagem_url": produto.imagem_url,
            "peso_produto_gramas": produto.peso_produto_gramas,
            "comprimento_centimetros": produto.comprimento_centimetros,
            "altura_centimetros": produto.altura_centimetros,
            "largura_centimetros": produto.largura_centimetros,
            "sales_count": int(sales_count or 0),
            "average_rating": float(average_rating or 0.0),
            "review_count": int(review_count or 0),
        }
        for produto, sales_count, average_rating, review_count in rows
    ]

    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
    }


@router.get("/categorias", response_model=list[str])
def listar_categorias_produto(db: Session = Depends(get_db)):
    categorias_raw = db.query(Produto.categoria_produto).distinct().all()
    return [categoria[0] for categoria in categorias_raw if categoria[0] is not None]


@router.get("/{id_produto}/detalhes", response_model=ProdutoDetalhesRead)
def buscar_produto_detalhes(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    order_ids_query = (
        db.query(ItemPedido.id_pedido)
        .filter(ItemPedido.id_produto == id_produto)
        .distinct()
    )

    sales_count = (
        db.query(func.count(ItemPedido.id_item))
        .filter(ItemPedido.id_produto == id_produto)
        .scalar()
        or 0
    )

    average_rating, review_count = (
        db.query(
            func.avg(AvaliacaoPedido.avaliacao),
            func.count(AvaliacaoPedido.id_avaliacao),
        )
        .filter(AvaliacaoPedido.id_pedido.in_(order_ids_query))
        .first()
        or (0.0, 0)
    )

    return {
        "id_produto": produto.id_produto,
        "nome_produto": produto.nome_produto,
        "categoria_produto": produto.categoria_produto,
        "imagem_url": produto.imagem_url,
        "peso_produto_gramas": produto.peso_produto_gramas,
        "comprimento_centimetros": produto.comprimento_centimetros,
        "altura_centimetros": produto.altura_centimetros,
        "largura_centimetros": produto.largura_centimetros,
        "sales_count": int(sales_count or 0),
        "average_rating": float(average_rating or 0.0),
        "review_count": int(review_count or 0),
    }


@router.get("/{id_produto}/avaliacoes", response_model=ProdutoAvaliacoesPaginatedRead)
def listar_avaliacoes_produto(
    id_produto: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
):
    produto_existe = db.query(Produto.id_produto).filter(Produto.id_produto == id_produto).first()
    if not produto_existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    order_ids_query = (
        db.query(ItemPedido.id_pedido)
        .filter(ItemPedido.id_produto == id_produto)
        .distinct()
    )

    reviews_query = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_pedido.in_(order_ids_query))

    total_items = reviews_query.count()
    total_pages = max(1, ceil(total_items / page_size))

    if page > total_pages:
        page = total_pages

    reviews = (
        reviews_query
        .order_by(AvaliacaoPedido.data_comentario.desc(), AvaliacaoPedido.id_avaliacao.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": reviews,
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
    }


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

    db.query(ItemPedido).filter(ItemPedido.id_produto == id_produto).delete(synchronize_session=False)
    db.delete(produto)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível excluir este produto devido a vínculos existentes",
        )

    return None