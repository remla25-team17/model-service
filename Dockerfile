FROM python:3

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code
COPY src/ /app/

# Expose port
EXPOSE 8080

# Model version
ARG MODEL_SERVICE_VERSION=0.0.0
ENV MODEL_SERVICE_VERSION=${MODEL_SERVICE_VERSION}

ENTRYPOINT ["python"]
CMD ["main.py"]
