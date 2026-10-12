FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install system dependencies, including OpenCV requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first to use Docker's build cache
COPY pyproject.toml uv.lock ./

# Install dependencies into the system Python environment
RUN uv sync --locked --no-install-project

# Copy the rest of the project
COPY . .

# Install the project itself
RUN uv sync --locked

EXPOSE 5000

CMD ["uv", "run", "--no-sync", "python", "app.py"]
