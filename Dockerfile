# Dockerfile for Quantum DevOps Toolchain
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY configs/ configs/
COPY README.md .
COPY setup.py .

# Install the package
RUN pip install --no-cache-dir -e .

# Expose port for web interface (if applicable)
EXPOSE 8000

# Default command
CMD ["python", "-c", "from src.main import get_toolchain; print('Quantum DevOps Toolchain is ready!')"]