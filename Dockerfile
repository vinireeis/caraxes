FROM python:3.12-slim

WORKDIR /src

COPY pyproject.toml poetry.lock alembic.ini ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["python3", "main.py"]
