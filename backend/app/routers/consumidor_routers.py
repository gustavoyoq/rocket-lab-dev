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
def create_consumer(payload: ConsumidorCreate, db: Session = Depends(get_db)):
    existing_consumer = db.query(Consumidor).filter(Consumidor.id_consumidor == payload.id_consumidor).first()

    if existing_consumer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ocorreu um erro na criação de consumidor (ID), tente novamente",
        )

    new_consumer = Consumidor(
        id_consumidor=payload.id_consumidor,
        prefixo_cep=payload.prefixo_cep,
        nome_consumidor=payload.nome_consumidor,
        cidade=payload.cidade,
        estado=payload.estado,
    )

    db.add(new_consumer)
    db.commit()
    db.refresh(new_consumer)

    return new_consumer


@router.get("", response_model=list[ConsumidorRead])
def list_consumers(db: Session = Depends(get_db)):
    consumers = db.query(Consumidor).all()
    return consumers


@router.get("/{id_consumidor}", response_model=ConsumidorRead)
def get_consumer_by_id(id_consumidor: str, db: Session = Depends(get_db)):
    consumer = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()

    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado",
        )

    return consumer


@router.patch("/{id_consumidor}", response_model=ConsumidorRead)
def update_consumer(
    id_consumidor: str,
    payload: ConsumidorUpdate,
    db: Session = Depends(get_db),
):
    consumer = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()

    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(consumer, field, value)

    db.commit()
    db.refresh(consumer)

    return consumer


@router.delete("/{id_consumidor}", status_code=status.HTTP_204_NO_CONTENT)
def delete_consumer(id_consumidor: str, db: Session = Depends(get_db)):
    consumer = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()

    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumidor não encontrado",
        )

    db.delete(consumer)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir este consumidor porque existem pedidos associados",
        )

    return None