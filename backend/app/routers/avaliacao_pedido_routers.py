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
def criar_avaliacao_pedido(payload: AvaliacaoPedidoCreate, db: Session = Depends(get_db)):
    avaliacao_existente = db.query(AvaliacaoPedido).filter(
        AvaliacaoPedido.id_avaliacao == payload.id_avaliacao
    ).first()
    if avaliacao_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ocorreu um erro na criação de avaliação de pedido (ID), tente novamente",
        )

    pedido = db.query(Pedido).filter(Pedido.id_pedido == payload.id_pedido).first()
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado para associar à avaliação",
        )

    nova_avaliacao = AvaliacaoPedido(
        id_avaliacao=payload.id_avaliacao,
        id_pedido=payload.id_pedido,
        avaliacao=payload.avaliacao,
        titulo_comentario=payload.titulo_comentario,
        comentario=payload.comentario,
        data_comentario=payload.data_comentario,
        data_resposta=payload.data_resposta,
    )

    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)

    return nova_avaliacao


@router.get("", response_model=list[AvaliacaoPedidoRead])
def listar_avaliacoes_pedidos(db: Session = Depends(get_db)):
    avaliacoes = db.query(AvaliacaoPedido).all()
    return avaliacoes


@router.get("/{id_avaliacao}", response_model=AvaliacaoPedidoRead)
def buscar_avaliacao_pedido_por_id(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_avaliacao == id_avaliacao).first()

    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação de pedido não encontrada",
        )

    return avaliacao


@router.patch("/{id_avaliacao}", response_model=AvaliacaoPedidoRead)
def atualizar_avaliacao_pedido(
    id_avaliacao: str,
    payload: AvaliacaoPedidoUpdate,
    db: Session = Depends(get_db),
):
    avaliacao = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_avaliacao == id_avaliacao).first()

    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação de pedido não encontrada",
        )

    dados_atualizacao = payload.model_dump(exclude_unset=True)

    if "id_pedido" in dados_atualizacao:
        pedido = db.query(Pedido).filter(Pedido.id_pedido == dados_atualizacao["id_pedido"]).first()
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado para associar à avaliação",
            )

    for campo, valor in dados_atualizacao.items():
        setattr(avaliacao, campo, valor)

    db.commit()
    db.refresh(avaliacao)

    return avaliacao


@router.delete("/{id_avaliacao}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_avaliacao_pedido(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao = db.query(AvaliacaoPedido).filter(AvaliacaoPedido.id_avaliacao == id_avaliacao).first()

    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação de pedido não encontrada",
        )

    db.delete(avaliacao)
    db.commit()

    return None