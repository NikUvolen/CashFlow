FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock /app/
COPY CashFlow /app/CashFlow

RUN uv sync --frozen --no-dev

WORKDIR /app/CashFlow

EXPOSE 8000

CMD ["sh", "-c", "uv run --frozen python manage.py migrate && uv run --frozen python manage.py collectstatic --noinput && uv run --frozen gunicorn CashFlow.wsgi:application --bind 0.0.0.0:8000"]
