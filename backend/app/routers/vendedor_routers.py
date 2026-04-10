from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendedor import Vendedor
from app.schemas.vendedor_schema import VendedorCreate, VendedorRead, VendedorUpdate

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])


@router.post("", response_model=VendedorRead, status_code=status.HTTP_201_CREATED)
def criar_vendedor(payload: VendedorCreate, db: Session = Depends(get_db)):
    vendedor_existente = db.query(Vendedor).filter(Vendedor.id_vendedor == payload.id_vendedor).first()

    if vendedor_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ocorreu um erro na criação de vendedor (ID), tente novamente",
        )

    novo_vendedor = Vendedor(
        id_vendedor=payload.id_vendedor,
        nome_vendedor=payload.nome_vendedor,
        prefixo_cep=payload.prefixo_cep,
        cidade=payload.cidade,
        estado=payload.estado,
    )

    db.add(novo_vendedor)
    db.commit()
    db.refresh(novo_vendedor)

    return novo_vendedor


@router.get("", response_model=list[VendedorRead])
def listar_vendedores(db: Session = Depends(get_db)):
    vendedores = db.query(Vendedor).all()
    return vendedores


@router.get("/{id_vendedor}", response_model=VendedorRead)
def buscar_vendedor_por_id(id_vendedor: str, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()

    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado",
        )

    return vendedor


@router.patch("/{id_vendedor}", response_model=VendedorRead)
def atualizar_vendedor(
    id_vendedor: str,
    payload: VendedorUpdate,
    db: Session = Depends(get_db),
):
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()

    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado",
        )

    dados_atualizacao = payload.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizacao.items():
        setattr(vendedor, campo, valor)

    db.commit()
    db.refresh(vendedor)

    return vendedor


@router.delete("/{id_vendedor}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_vendedor(id_vendedor: str, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()

    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado",
        )

    db.delete(vendedor)
    db.commit()

    return None