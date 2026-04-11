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


_imagens_por_categoria: dict[str, str] = {}


def _vazio_para_none(valor: str | None) -> str | None:
    if valor is None:
        return None
    valor = valor.strip()
    if valor == "" or valor.lower() == "null":
        return None
    return valor


def _para_inteiro(valor: str | None) -> int | None:
    processado = _vazio_para_none(valor)
    if processado is None:
        return None
    return int(processado)


def _para_float(valor: str | None) -> float | None:
    processado = _vazio_para_none(valor)
    if processado is None:
        return None
    return float(processado)


def _para_datetime(valor: str | None) -> datetime | None:
    processado = _vazio_para_none(valor)
    if processado is None:
        return None

    if processado.endswith("Z"):
        processado = processado.replace("Z", "+00:00")
    return datetime.fromisoformat(processado)


def _para_date(valor: str | None) -> date | None:
    processado = _vazio_para_none(valor)
    if processado is None:
        return None

    if processado.endswith("Z"):
        processado = processado.replace("Z", "+00:00")

    try:
        return date.fromisoformat(processado)
    except ValueError:
        return datetime.fromisoformat(processado).date()


def _obter_campo(row: dict[str, str], *nomes: str) -> str | None:
    for nome in nomes:
        if nome in row:
            return row.get(nome)
    return None


def _normalizar_categoria(valor: str | None) -> str:
    if valor is None:
        return ""
    return valor.strip().lower()


def _carregar_imagens_categoria(data_dir: Path) -> dict[str, str]:
    arquivo = data_dir / "dim_categoria_imagens.csv"
    if not arquivo.exists():
        return {}

    imagens: dict[str, str] = {}
    with arquivo.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            categoria = _obter_campo(row, "categoria", "Categoria")
            link = _obter_campo(row, "link", "Link")
            categoria_normalizada = _normalizar_categoria(categoria)
            if categoria_normalizada and link:
                imagens[categoria_normalizada] = link.strip()

    return imagens


def _map_consumidor(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id_consumidor": row["id_consumidor"],
        "prefixo_cep": row["prefixo_cep"],
        "nome_consumidor": row["nome_consumidor"],
        "cidade": row["cidade"],
        "estado": row["estado"],
    }


def _map_produto(row: dict[str, str]) -> dict[str, Any]:
    categoria = row["categoria_produto"]
    imagem_url = _imagens_por_categoria.get(_normalizar_categoria(categoria))

    return {
        "id_produto": row["id_produto"],
        "nome_produto": row["nome_produto"],
        "categoria_produto": categoria,
        "imagem_url": imagem_url,
        "peso_produto_gramas": _para_float(row.get("peso_produto_gramas")),
        "comprimento_centimetros": _para_float(row.get("comprimento_centimetros")),
        "altura_centimetros": _para_float(row.get("altura_centimetros")),
        "largura_centimetros": _para_float(row.get("largura_centimetros")),
    }


def _map_vendedor(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id_vendedor": row["id_vendedor"],
        "nome_vendedor": row["nome_vendedor"],
        "prefixo_cep": row["prefixo_cep"],
        "cidade": row["cidade"],
        "estado": row["estado"],
    }


def _map_pedido(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id_pedido": row["id_pedido"],
        "id_consumidor": row["id_consumidor"],
        "status": _obter_campo(row, "status", "status_pedido"),
        "pedido_compra_timestamp": _para_datetime(
            _obter_campo(row, "pedido_compra_timestamp", "timestamp_compra_pedido")
        ),
        "pedido_entregue_timestamp": _para_datetime(
            _obter_campo(row, "pedido_entregue_timestamp", "data_entrega_pedido_consumidor")
        ),
        "data_estimada_entrega": _para_date(
            _obter_campo(row, "data_estimada_entrega", "data_estimada_entrega_pedido")
        ),
        "tempo_entrega_dias": _para_float(_obter_campo(row, "tempo_entrega_dias", "tempo_entregue_dias")),
        "tempo_entrega_estimado_dias": _para_float(row.get("tempo_entrega_estimado_dias")),
        "diferenca_entrega_dias": _para_float(row.get("diferenca_entrega_dias")),
        "entrega_no_prazo": row.get("entrega_no_prazo"),
    }


def _map_item_pedido(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id_pedido": row["id_pedido"],
        "id_item": _para_inteiro(row.get("id_item")),
        "id_produto": row["id_produto"],
        "id_vendedor": row["id_vendedor"],
        "preco_BRL": _para_float(row.get("preco_BRL")),
        "preco_frete": _para_float(row.get("preco_frete")),
    }


def _map_avaliacao_pedido(row: dict[str, str]) -> dict[str, Any] | None:
    nota_bruta = _obter_campo(row, "avaliacao", "nota_avaliacao", "nota_avaliaco")

    try:
        avaliacao = _para_inteiro(nota_bruta)
    except ValueError:
        return None

    return {
        "id_avaliacao": row["id_avaliacao"],
        "id_pedido": row["id_pedido"],
        "avaliacao": avaliacao,
        "titulo_comentario": _obter_campo(row, "titulo_comentario", "titulo_avaliacao_comentario"),
        "comentario": _obter_campo(row, "comentario", "mensagem_avaliacao_comentario"),
        "data_comentario": _para_datetime(_obter_campo(row, "data_comentario", "data_criacao_avaliacao")),
        "data_resposta": _para_datetime(_obter_campo(row, "data_resposta", "data_resposta_avaliacao")),
    }


DatasetMapper = Callable[[dict[str, str]], dict[str, Any] | None]


DATASETS: list[tuple[str, str, Any, DatasetMapper]] = [
    ("consumidores", "dim_consumidores.csv", Consumidor, _map_consumidor),
    ("produtos", "dim_produtos.csv", Produto, _map_produto),
    ("vendedores", "dim_vendedores.csv", Vendedor, _map_vendedor),
    ("pedidos", "fat_pedidos.csv", Pedido, _map_pedido),
    ("itens_pedidos", "fat_itens_pedidos.csv", ItemPedido, _map_item_pedido),
    ("avaliacoes_pedidos", "fat_avaliacoes_pedidos.csv", AvaliacaoPedido, _map_avaliacao_pedido),
]


TRUNCATE_ORDER = [
    AvaliacaoPedido,
    ItemPedido,
    Pedido,
    Vendedor,
    Produto,
    Consumidor,
]


def ingerir_dados_csv(db: Session, data_dir: Path, truncate_before_load: bool = False) -> dict[str, int]:
    if not data_dir.exists():
        raise FileNotFoundError(f"Diretorio de dados nao encontrado: {data_dir}")

    global _imagens_por_categoria
    _imagens_por_categoria = _carregar_imagens_categoria(data_dir)

    if truncate_before_load:
        for model in TRUNCATE_ORDER:
            db.execute(delete(model))
        db.commit()

    resumo: dict[str, int] = {}

    for table_nome, filename, model, mapper in DATASETS:
        csv_path = data_dir / filename
        if not csv_path.exists():
            raise FileNotFoundError(f"Arquivo CSV nao encontrado: {csv_path}")

        rows: list[dict[str, Any]] = []
        with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                linha_mapeada = mapper(row)
                if linha_mapeada is None:
                    continue
                rows.append(linha_mapeada)

        if rows:
            db.execute(insert(model).prefix_with("OR IGNORE"), rows)
            db.commit()

        resumo[table_nome] = len(rows)

    return resumo
