# Rocket Lab Dev

Aplicacao full stack com:

- Backend em FastAPI + SQLAlchemy + Alembic
- Frontend em React + Vite + TypeScript
- Banco SQLite local

## Requisitos

- Python 3.11+
- Node.js 18+
- pnpm (ou npm)

## Estrutura

- backend/: API, models, migrations e banco SQLite
- frontend/rocket-lab-dev/: interface web

## 1. Instalar o backend

Na raiz do projeto, entre na pasta backend:

```bash
cd backend
```

Crie e ative o ambiente virtual.

Windows (PowerShell):

```bash
python -m venv ..\venv
..\venv\Scripts\Activate.ps1
```

Windows (CMD):

```bash
python -m venv ..\venv
..\venv\Scripts\activate.bat
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Rode as migrations:

```bash
alembic upgrade head
```

## 2. Popular o banco de dados (scripts)

Com o ambiente virtual ativo e ainda em backend/, execute a carga dos CSVs:

```bash
python -m app.scripts.ingest_csv
```

Esse comando le os arquivos em backend/data e insere os dados no banco.

Se quiser limpar as tabelas antes de carregar novamente:

```bash
python -m app.scripts.ingest_csv --truncate
```

Se os arquivos estiverem em outro diretorio:

```bash
python -m app.scripts.ingest_csv --data-dir "C:/caminho/para/csvs"
```

## 3. Rodar o backend

Ainda em backend/:

```bash
python -m app.main
```

A API sobe em:

- http://localhost:8000

Documentacao interativa:

- http://localhost:8000/docs

## 4. Instalar o frontend

Em outro terminal, na raiz do projeto:

```bash
cd frontend/rocket-lab-dev
pnpm install
```

Opcional: configurar URL da API criando arquivo .env na pasta frontend/rocket-lab-dev:

```bash
VITE_API_URL=http://localhost:8000
```

Se nao configurar, o frontend usa http://localhost:8000 por padrao.

## 5. Rodar o frontend

Na pasta frontend/rocket-lab-dev:

```bash
pnpm dev
```

Abra no navegador:

- http://localhost:5173

## Scripts uteis do frontend

Na pasta frontend/rocket-lab-dev:

- Desenvolvimento: pnpm dev
- Build: pnpm build
- Preview de build: pnpm preview
- Lint: pnpm lint

## Fluxo rapido (resumo)

Terminal 1:

```bash
cd backend
..\venv\Scripts\Activate.ps1
python -m app.main
```

Terminal 2:

```bash
cd frontend/rocket-lab-dev
pnpm dev
```

Pronto: frontend em 5173 consumindo backend em 8000.
