FROM python:3.12-slim

WORKDIR /src

COPY ./pyproject.toml ./poetry.lock /src/

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY ./src /src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
