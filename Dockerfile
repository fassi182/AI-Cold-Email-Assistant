# Use an official lightweight Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install compilation tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the src folder containing backend.py and ai_logic.py
COPY src/ ./src/

# Expose port 10000 (Render's default)
EXPOSE 10000

# Start Uvicorn and bind it to the $PORT variable provided by Render
CMD ["sh", "-c", "uvicorn src.backend:app --host 0.0.0.0 --port ${PORT:-10000}"]