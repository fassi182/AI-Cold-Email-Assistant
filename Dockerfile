# Use an official lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and force clean logging output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade system tools and install ALL necessary compilation libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your internal application code folder
COPY src/ ./src/

# Expose port 8080 (standard cloud container runtime port)
EXPOSE 8080

# Boot up Uvicorn with workers for production traffic
CMD ["uvicorn", "src.backend:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]