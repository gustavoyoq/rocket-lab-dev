from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.models.vendedor import Vendedor
from app.schemas.item_pedido_schema import ItemPedidoCreate, ItemPedidoRead, ItemPedidoUpdate

router = APIRouter(prefix="/itens-pedidos", tags=["ItensPedidos"])


@router.post("", response_model=ItemPedidoRead, status_code=status.HTTP_201_CREATED)
def create_order_item(payload: ItemPedidoCreate, db: Session = Depends(get_db)):
    order = db.query(Pedido).filter(Pedido.id_pedido == payload.id_pedido).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado para associar ao item",
        )

    product = db.query(Produto).filter(Produto.id_produto == payload.id_produto).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado para associar ao item",
        )

    seller = db.query(Vendedor).filter(Vendedor.id_vendedor == payload.id_vendedor).first()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor não encontrado para associar ao item",
        )

    new_item = ItemPedido(
        id_pedido=payload.id_pedido,
        id_item=payload.id_item,
        id_produto=payload.id_produto,
        id_vendedor=payload.id_vendedor,
        preco_BRL=payload.preco_BRL,
        preco_frete=payload.preco_frete,
    )

    db.add(new_item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ocorreu um erro na criação do item de pedido, verifique os identificadores informados",
        )
    db.refresh(new_item)

    return new_item


@router.get("", response_model=list[ItemPedidoRead])
def list_order_items(db: Session = Depends(get_db)):
    items = db.query(ItemPedido).all()
    return items


@router.get("/{id_pedido}/{id_item}", response_model=ItemPedidoRead)
def get_order_item_by_id(id_pedido: str, id_item: int, db: Session = Depends(get_db)):
    item = db.query(ItemPedido).filter(
        ItemPedido.id_pedido == id_pedido,
        ItemPedido.id_item == id_item,
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de pedido não encontrado",
        )

    return item


@router.patch("/{id_pedido}/{id_item}", response_model=ItemPedidoRead)
def update_order_item(
    id_pedido: str,
    id_item: int,
    payload: ItemPedidoUpdate,
    db: Session = Depends(get_db),
):
    item = db.query(ItemPedido).filter(
        ItemPedido.id_pedido == id_pedido,
        ItemPedido.id_item == id_item,
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de pedido não encontrado",
        )

    update_data = payload.model_dump(exclude_unset=True)

    if "id_produto" in update_data:
        product = db.query(Produto).filter(Produto.id_produto == update_data["id_produto"]).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado para associar ao item",
            )

    if "id_vendedor" in update_data:
        seller = db.query(Vendedor).filter(Vendedor.id_vendedor == update_data["id_vendedor"]).first()
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vendedor não encontrado para associar ao item",
            )

    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{id_pedido}/{id_item}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(id_pedido: str, id_item: int, db: Session = Depends(get_db)):
    item = db.query(ItemPedido).filter(
        ItemPedido.id_pedido == id_pedido,
        ItemPedido.id_item == id_item,
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de pedido não encontrado",
        )

    db.delete(item)
    db.commit()

    return None