FROM astral/uv:latest AS uv_builder

FROM python:3.11-slim

WORKDIR /app

COPY --from=uv_builder /uv /uvx /bin/

COPY . .

# Create virtual environment and add it to PATH
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN python3 -m venv $UV_PROJECT_ENVIRONMENT
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

RUN uv sync --locked

EXPOSE 5000

CMD ["python", "app.py"]
