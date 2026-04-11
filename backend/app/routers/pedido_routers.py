from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.consumidor import Consumidor
from app.models.pedido import Pedido
from app.schemas.pedido_schema import PedidoCreate, PedidoRead, PedidoUpdate

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def criar_pedido(payload: PedidoCreate, db: Session = Depends(get_db)):
    pedido_existente = db.query(Pedido).filter(Pedido.id_pedido == payload.id_pedido).first()
    if pedido_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ocorreu um erro na criação de pedido (ID), tente novamente",
        )

    consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == payload.id_consumidor).first()
    if not consumidor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado para associar ao pedido",
        )

    novo_pedido = Pedido(
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

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido


@router.get("", response_model=list[PedidoRead])
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).all()
    return pedidos


@router.get("/{id_pedido}", response_model=PedidoRead)
def buscar_pedido_por_id(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )

    return pedido


@router.patch("/{id_pedido}", response_model=PedidoRead)
def atualizar_pedido(
    id_pedido: str,
    payload: PedidoUpdate,
    db: Session = Depends(get_db),
):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )

    dados_atualizacao = payload.model_dump(exclude_unset=True)

    if "id_consumidor" in dados_atualizacao:
        consumidor = db.query(Consumidor).filter(
            Consumidor.id_consumidor == dados_atualizacao["id_consumidor"]
        ).first()
        if not consumidor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consumidor não encontrado para associar ao pedido",
            )

    for campo, valor in dados_atualizacao.items():
        setattr(pedido, campo, valor)

    db.commit()
    db.refresh(pedido)

    return pedido


@router.delete("/{id_pedido}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )

    db.delete(pedido)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir este pedido porque existem itens de pedido ou avaliações associadas",
        )

    return None