FROM python:3.11-slim AS builder

# curl and uv
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get remove -y curl && apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create venv and install dependencies
RUN uv venv /opt/venv && \
    uv pip install --python /opt/venv/bin/python --no-cache-dir fastapi uvicorn[standard] pydantic

FROM python:3.11-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy venvfrom builder
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser api/ ./api/

# Use venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app"

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]