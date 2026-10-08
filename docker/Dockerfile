# Supply Chain Digital Twin - Flask Application
# Review 1: Basic containerized application with frontend

# Stage 1: Base image
FROM python:3.11-slim AS base

# Set metadata
LABEL maintainer="Supply Chain DT Team"
LABEL version="0.1.0"
LABEL description="Supply Chain Digital Twin - Flask API with Frontend"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Set working directory
WORKDIR /app

# Install system dependencies (curl needed for HEALTHCHECK)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Copy static frontend files
COPY static/ ./static/

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]
