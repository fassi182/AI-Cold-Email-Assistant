# Use an official lightweight Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system compilation tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the src folder into the container
COPY src/ ./src/

# Expose port 7860 (Hugging Face Spaces standard port)
EXPOSE 7860

# Run uvicorn pointing to backend.py inside the src folder
CMD ["uvicorn", "src.backend:app", "--host", "0.0.0.0", "--port", "7860"]