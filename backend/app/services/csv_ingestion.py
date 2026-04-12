from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable

from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from app.models.avaliacao_pedido import AvaliacaoPedido
from app.models.consumidor import Consumidor
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.models.vendedor import Vendedor


_images_by_category: dict[str, str] = {}


def _empty_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if value == "" or value.lower() == "null":
        return None
    return value


def _to_int(value: str | None) -> int | None:
    parsed = _empty_to_none(value)
    if parsed is None:
        return None
    return int(parsed)


def _to_float(value: str | None) -> float | None:
    parsed = _empty_to_none(value)
    if parsed is None:
        return None
    return float(parsed)


def _to_datetime(value: str | None) -> datetime | None:
    parsed = _empty_to_none(value)
    if parsed is None:
        return None

    if parsed.endswith("Z"):
        parsed = parsed.replace("Z", "+00:00")
    return datetime.fromisoformat(parsed)


def _to_date(value: str | None) -> date | None:
    parsed = _empty_to_none(value)
    if parsed is None:
        return None

    if parsed.endswith("Z"):
        parsed = parsed.replace("Z", "+00:00")

    try:
        return date.fromisoformat(parsed)
    except ValueError:
        return datetime.fromisoformat(parsed).date()


def _get_field(row: dict[str, str], *names: str) -> str | None:
    for name in names:
        if name in row:
            return row.get(name)
    return None


def _normalize_category(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip().lower()


def _load_category_images(data_dir: Path) -> dict[str, str]:
    file_path = data_dir / "dim_categoria_imagens.csv"
    if not file_path.exists():
        return {}

    images: dict[str, str] = {}
    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            category = _get_field(row, "categoria", "Categoria")
            link = _get_field(row, "link", "Link")
            normalized_category = _normalize_category(category)
            if normalized_category and link:
                images[normalized_category] = link.strip()

    return images


def _map_consumer(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id_consumidor": row["id_consumidor"],
        "prefixo_cep": row["prefixo_cep"],
        "nome_consumidor": row["nome_consumidor"],
        "cidade": row["cidade"],
        "estado": row["estado"],
    }


def _map_product(row: dict[str, str]) -> dict[str, Any]:
    category = (row.get("categoria_produto") or "").strip()
    if category == "":
        category = "sem_categoria"

    image_url = _images_by_category.get(_normalize_category(category))

    return {
        "id_produto": row["id_produto"],
        "nome_produto": row["nome_produto"],
        "categoria_produto": category,
        "imagem_url": image_url,
        "peso_produto_gramas": _to_float(row.get("peso_produto_gramas")),
        "comprimento_centimetros": _to_float(row.get("comprimento_centimetros")),
        "altura_centimetros": _to_float(row.get("altura_centimetros")),
        "largura_centimetros": _to_float(row.get("largura_centimetros")),
    }


def _map_seller(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id_vendedor": row["id_vendedor"],
        "nome_vendedor": row["nome_vendedor"],
        "prefixo_cep": row["prefixo_cep"],
        "cidade": row["cidade"],
        "estado": row["estado"],
    }


def _map_order(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id_pedido": row["id_pedido"],
        "id_consumidor": row["id_consumidor"],
        "status": _get_field(row, "status", "status_pedido"),
        "pedido_compra_timestamp": _to_datetime(
            _get_field(row, "pedido_compra_timestamp", "timestamp_compra_pedido")
        ),
        "pedido_entregue_timestamp": _to_datetime(
            _get_field(row, "pedido_entregue_timestamp", "data_entrega_pedido_consumidor")
        ),
        "data_estimada_entrega": _to_date(
            _get_field(row, "data_estimada_entrega", "data_estimada_entrega_pedido")
        ),
        "tempo_entrega_dias": _to_float(_get_field(row, "tempo_entrega_dias", "tempo_entregue_dias")),
        "tempo_entrega_estimado_dias": _to_float(row.get("tempo_entrega_estimado_dias")),
        "diferenca_entrega_dias": _to_float(row.get("diferenca_entrega_dias")),
        "entrega_no_prazo": row.get("entrega_no_prazo"),
    }


def _map_order_item(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id_pedido": row["id_pedido"],
        "id_item": _to_int(row.get("id_item")),
        "id_produto": row["id_produto"],
        "id_vendedor": row["id_vendedor"],
        "preco_BRL": _to_float(row.get("preco_BRL")),
        "preco_frete": _to_float(row.get("preco_frete")),
    }


def _map_order_review(row: dict[str, str]) -> dict[str, Any] | None:
    raw_rating = _get_field(row, "avaliacao", "nota_avaliacao", "nota_avaliaco")

    try:
        rating = _to_int(raw_rating)
    except ValueError:
        return None

    return {
        "id_avaliacao": row["id_avaliacao"],
        "id_pedido": row["id_pedido"],
        "avaliacao": rating,
        "titulo_comentario": _get_field(row, "titulo_comentario", "titulo_avaliacao_comentario"),
        "comentario": _get_field(row, "comentario", "mensagem_avaliacao_comentario"),
        "data_comentario": _to_datetime(_get_field(row, "data_comentario", "data_criacao_avaliacao")),
        "data_resposta": _to_datetime(_get_field(row, "data_resposta", "data_resposta_avaliacao")),
    }


DatasetMapper = Callable[[dict[str, str]], dict[str, Any] | None]


DATASETS: list[tuple[str, str, Any, DatasetMapper]] = [
    ("consumidores", "dim_consumidores.csv", Consumidor, _map_consumer),
    ("produtos", "dim_produtos.csv", Produto, _map_product),
    ("vendedores", "dim_vendedores.csv", Vendedor, _map_seller),
    ("pedidos", "fat_pedidos.csv", Pedido, _map_order),
    ("itens_pedidos", "fat_itens_pedidos.csv", ItemPedido, _map_order_item),
    ("avaliacoes_pedidos", "fat_avaliacoes_pedidos.csv", AvaliacaoPedido, _map_order_review),
]


TRUNCATE_ORDER = [
    AvaliacaoPedido,
    ItemPedido,
    Pedido,
    Vendedor,
    Produto,
    Consumidor,
]


def ingest_csv_data(db: Session, data_dir: Path, truncate_before_load: bool = False) -> dict[str, int]:
    if not data_dir.exists():
        raise FileNotFoundError(f"Diretorio de dados nao encontrado: {data_dir}")

    global _images_by_category
    _images_by_category = _load_category_images(data_dir)

    if truncate_before_load:
        for model in TRUNCATE_ORDER:
            db.execute(delete(model))
        db.commit()

    summary: dict[str, int] = {}

    for table_name, filename, model, mapper in DATASETS:
        csv_path = data_dir / filename
        if not csv_path.exists():
            raise FileNotFoundError(f"Arquivo CSV nao encontrado: {csv_path}")

        rows: list[dict[str, Any]] = []
        with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                mapped_row = mapper(row)
                if mapped_row is None:
                    continue
                rows.append(mapped_row)

        if rows:
            db.execute(insert(model).prefix_with("OR IGNORE"), rows)
            db.commit()

        summary[table_name] = len(rows)

    return summary
