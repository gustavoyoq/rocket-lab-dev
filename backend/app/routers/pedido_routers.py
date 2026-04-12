from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.consumidor import Consumidor
from app.models.pedido import Pedido
from app.schemas.pedido_schema import PedidoCreate, PedidoRead, PedidoUpdate

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: PedidoCreate, db: Session = Depends(get_db)):
    existing_order = db.query(Pedido).filter(Pedido.id_pedido == payload.id_pedido).first()
    if existing_order:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ocorreu um erro na criação de pedido (ID), tente novamente",
        )

    consumer = db.query(Consumidor).filter(Consumidor.id_consumidor == payload.id_consumidor).first()
    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado para associar ao pedido",
        )

    new_order = Pedido(
        id_pedido=payload.id_pedido,
        id_consumidor=payload.id_consumidor,
        status=payload.status,
        pedido_compra_timestamp=payload.pedido_compra_timestamp,
        pedido_entregue_timestamp=payload.pedido_entregue_timestamp,
        data_estimada_entrega=payload.data_estimada_entrega,
        tempo_entrega_dias=payload.tempo_entrega_dias,
        tempo_entrega_estimado_dias=payload.tempo_entrega_estimado_dias,
        diferenca_entrega_dias=payload.diferenca_entrega_dias,
        entrega_no_prazo=payload.entrega_no_prazo,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("", response_model=list[PedidoRead])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(Pedido).all()
    return orders


@router.get("/{id_pedido}", response_model=PedidoRead)
def get_order_by_id(id_pedido: str, db: Session = Depends(get_db)):
    order = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )

    return order


@router.patch("/{id_pedido}", response_model=PedidoRead)
def update_order(
    id_pedido: str,
    payload: PedidoUpdate,
    db: Session = Depends(get_db),
):
    order = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )

    update_data = payload.model_dump(exclude_unset=True)

    if "id_consumidor" in update_data:
        consumer = db.query(Consumidor).filter(
            Consumidor.id_consumidor == update_data["id_consumidor"]
        ).first()
        if not consumer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consumidor não encontrado para associar ao pedido",
            )

    for field, value in update_data.items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)

    return order


@router.delete("/{id_pedido}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id_pedido: str, db: Session = Depends(get_db)):
    order = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )

    db.delete(order)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir este pedido porque existem itens de pedido ou avaliações associadas",
        )

    return None