from __future__ import annotations

import argparse
from pathlib import Path

from app.database import SessionLocal
from app.services.csv_ingestion import ingerir_dados_csv


def _default_data_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "data"


def main() -> None:
    parse = argparse.ArgumentParser(description="Ingestao de CSVs para o banco de dados")
    parse.add_argument(
        "--data-dir",
        type=Path,
        default=_default_data_dir(),
        help="Diretorio com arquivos CSV (padrao: backend/data)",
    )
    parse.add_argument(
        "--truncate",
        action="store_true",
        help="Limpa as tabelas antes da carga",
    )
    args = parse.parse_args()

    sessao = SessionLocal()
    try:
        resumo = ingerir_dados_csv(
            db=sessao,
            data_dir=args.data_dir,
            truncate_before_load=args.truncate,
        )
    finally:
        sessao.close()

    print("Carga concluida com sucesso.")
    for table_nome, row_count in resumo.items():
        print(f"- {table_nome}: {row_count} linhas processadas")


if __name__ == "__main__":
    main()
