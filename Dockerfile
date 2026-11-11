FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and source files
COPY pyproject.toml .
COPY api ./api
COPY data ./data
COPY indexes ./indexes
COPY integration ./integration
COPY processing ./processing
COPY scientific ./scientific
COPY scripts ./scripts
COPY shared ./shared
COPY src ./src

# Install python dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic numpy sentence-transformers pytest

EXPOSE 8000

ENV PYTHONPATH="/app:/app/src"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
