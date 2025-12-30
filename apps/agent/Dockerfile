FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/

# Install dependencies as root
RUN pip install --no-cache-dir --upgrade pip && \
 pip install --no-cache-dir "uvicorn[standard]" && \
    pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add local bin to PATH for the non-root user
ENV PATH="/home/appuser/.local/bin:${PATH}"

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "-m", "uvicorn", "src.pmm_agent.server:app", "--host", "0.0.0.0", "--port", "8080"]
