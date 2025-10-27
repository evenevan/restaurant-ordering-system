FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false

RUN poetry install --only main --no-interaction --no-ansi

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

COPY backend/ ./backend/

USER appuser

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "-m", "backend"]
