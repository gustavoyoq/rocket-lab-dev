from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendedor import Vendedor
from app.schemas.vendedor_schema import VendedorCreate, VendedorRead, VendedorUpdate

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])


@router.post("", response_model=VendedorRead, status_code=status.HTTP_201_CREATED)
def create_seller(payload: VendedorCreate, db: Session = Depends(get_db)):
    existing_seller = db.query(Vendedor).filter(Vendedor.id_vendedor == payload.id_vendedor).first()

    if existing_seller:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ocorreu um erro na criação de vendedor (ID), tente novamente",
        )

    new_seller = Vendedor(
        id_vendedor=payload.id_vendedor,
        nome_vendedor=payload.nome_vendedor,
        prefixo_cep=payload.prefixo_cep,
        cidade=payload.cidade,
        estado=payload.estado,
    )

    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    return new_seller


@router.get("", response_model=list[VendedorRead])
def list_sellers(db: Session = Depends(get_db)):
    sellers = db.query(Vendedor).all()
    return sellers


@router.get("/{id_vendedor}", response_model=VendedorRead)
def get_seller_by_id(id_vendedor: str, db: Session = Depends(get_db)):
    seller = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()

    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado",
        )

    return seller


@router.patch("/{id_vendedor}", response_model=VendedorRead)
def update_seller(
    id_vendedor: str,
    payload: VendedorUpdate,
    db: Session = Depends(get_db),
):
    seller = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()

    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(seller, field, value)

    db.commit()
    db.refresh(seller)

    return seller


@router.delete("/{id_vendedor}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seller(id_vendedor: str, db: Session = Depends(get_db)):
    seller = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()

    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado",
        )

    db.delete(seller)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir este vendedor porque existem itens de pedido associados",
        )

    return None