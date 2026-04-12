from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.models.pedido import Pedido
from app.schemas.avaliacao_pedido_schema import (
    AvaliacaoPedidoCreate,
    AvaliacaoPedidoRead,
    AvaliacaoPedidoUpdate,
)

router = APIRouter(prefix="/avaliacoes-pedidos", tags=["AvaliacoesPedidos"])


@router.post("", response_model=AvaliacaoPedidoRead, status_code=status.HTTP_201_CREATED)
def create_order_review(payload: AvaliacaoPedidoCreate, db: Session = Depends(get_db)):
    existing_review = db.query(AvaliacaoPedido).filter(
        AvaliacaoPedido.id_avaliacao == payload.id_avaliacao
    ).first()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ocorreu um erro na criação de avaliação de pedido (ID), tente novamente",
        )

    order = db.query(Pedido).filter(Pedido.id_pedido == payload.id_pedido).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado para associar à avaliação",
        )

    new_review = AvaliacaoPedido(
        id_avaliacao=payload.id_avaliacao,
        id_pedido=payload.id_pedido,
        avaliacao=payload.avaliacao,
        titulo_comentario=payload.titulo_comentario,
        comentario=payload.comentario,
        data_comentario=payload.data_comentario,
        data_resposta=payload.data_resposta,
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


@router.get("", response_model=list[AvaliacaoPedidoRead])
def list_order_reviews(db: Session = Depends(get_db)):
    reviews = db.query(AvaliacaoPedido).all()
    return reviews


@router.get("/{id_avaliacao}", response_model=AvaliacaoPedidoRead)
def get_order_review_by_id(id_avaliacao: str, db: Session = Depends(get_db)):
    review = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_avaliacao == id_avaliacao).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação de pedido não encontrada",
        )

    return review


@router.patch("/{id_avaliacao}", response_model=AvaliacaoPedidoRead)
def update_order_review(
    id_avaliacao: str,
    payload: AvaliacaoPedidoUpdate,
    db: Session = Depends(get_db),
):
    review = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_avaliacao == id_avaliacao).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação de pedido não encontrada",
        )

    update_data = payload.model_dump(exclude_unset=True)

    if "id_pedido" in update_data:
        order = db.query(Pedido).filter(Pedido.id_pedido == update_data["id_pedido"]).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado para associar à avaliação",
            )

    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)

    return review


@router.delete("/{id_avaliacao}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_review(id_avaliacao: str, db: Session = Depends(get_db)):
    review = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_avaliacao == id_avaliacao).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação de pedido não encontrada",
        )

    db.delete(review)
    db.commit()

    return None