# Use official lightweight Python image
FROM python:3.13-slim

# Copy the uv binary directly from official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency definition first for optimal Docker layer caching
COPY pyproject.toml uv.lock* ./

# Install dependencies into system Python using uv (blazing fast)
RUN uv pip install --system -r pyproject.toml

# Copy application source code
COPY . .

# Expose FastAPI application port
EXPOSE 8000

# Run Uvicorn pointing to app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
