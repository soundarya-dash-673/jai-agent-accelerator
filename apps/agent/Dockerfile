FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy all necessary files
COPY pyproject.toml ./
COPY src/ ./src/

# Create README.md if pyproject.toml requires it
RUN echo "# PMM Agent" > README.md

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Security: non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8123

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8123}/health || exit 1

CMD uvicorn src.pmm_agent.server:app --host 0.0.0.0 --port ${PORT:-8123}