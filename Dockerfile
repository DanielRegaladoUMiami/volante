# Volante — FastAPI (backend + frontend) for a Hugging Face Docker Space.
FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# Install dependencies (cached layer)
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev

# App assets
COPY site ./site

ENV PYTHONPATH=/app/src \
    SITE_DIR=/app/site \
    DATABASE_URL=sqlite:////app/volante.db

# HF Spaces expect the app on 7860. Enable persistent storage and set
# DATABASE_URL=sqlite:////data/volante.db in the Space Secrets so rows survive restarts.
EXPOSE 7860
CMD ["/app/.venv/bin/uvicorn", "volante.main:app", "--host", "0.0.0.0", "--port", "7860"]
