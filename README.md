# FastApi

## Requirements:

- Docker CE/Desktop 20 or above

- Python 3.11

- [pipx](https://pipx.pypa.io/stable/installation/) and [poetry](https://python-poetry.org/docs/#installing-with-pipx)

## Development:

0. Prepare

- Install dependencies: `poetry install`
- Activate venv: `poetry shell`

1. Install lib

- production: `poetry add <lib-name>`
- dev: `poetry add -Gdev <lib-name>`

2. Run
- Run in local:
  - start compose stack for local database: `docker compose up -d`
  - start local server: `poetry run start`
      - server's running in: _localhost:8000_
      - swagger: _localhost:8000/docs_

3. Migration

    Make sure you're in venv shell: `poetry shell`

- Generate new migration: `alembic revision --autogenerate -m "<message here>"`
- Run migration: `alembic upgrade head`
