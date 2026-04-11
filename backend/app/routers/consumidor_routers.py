from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.consumidor import Consumidor
from app.schemas.consumidor_schema import (
    ConsumidorCreate,
    ConsumidorRead,
    ConsumidorUpdate,
)

router = APIRouter(prefix="/consumidores", tags=["Consumidores"])


@router.post("", response_model=ConsumidorRead, status_code=status.HTTP_201_CREATED)
def criar_consumidor(payload: ConsumidorCreate, db: Session = Depends(get_db)):
    consumidor_existente = db.query(Consumidor).filter(Consumidor.id_consumidor == payload.id_consumidor).first()

    if consumidor_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ocorreu um erro na criação de consumidor (ID), tente novamente",
        )

    novo_consumidor = Consumidor(
        id_consumidor=payload.id_consumidor,
        prefixo_cep=payload.prefixo_cep,
        nome_consumidor=payload.nome_consumidor,
        cidade=payload.cidade,
        estado=payload.estado,
    )

    db.add(novo_consumidor)
    db.commit()
    db.refresh(novo_consumidor)

    return novo_consumidor


@router.get("", response_model=list[ConsumidorRead])
def listar_consumidores(db: Session = Depends(get_db)):
    consumidores = db.query(Consumidor).all()
    return consumidores


@router.get("/{id_consumidor}", response_model=ConsumidorRead)
def buscar_consumidor_por_id(id_consumidor: str, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()

    if not consumidor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado",
        )

    return consumidor


@router.patch("/{id_consumidor}", response_model=ConsumidorRead)
def atualizar_consumidor(
    id_consumidor: str,
    payload: ConsumidorUpdate,
    db: Session = Depends(get_db),
):
    consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()

    if not consumidor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado",
        )

    dados_atualizacao = payload.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizacao.items():
        setattr(consumidor, campo, valor)

    db.commit()
    db.refresh(consumidor)

    return consumidor


@router.delete("/{id_consumidor}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_consumidor(id_consumidor: str, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()

    if not consumidor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado",
        )

    db.delete(consumidor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir este consumidor porque existem pedidos associados",
        )

    return None