FROM python:3

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code
COPY src/ .

# Expose port
EXPOSE 8080

# Model version
ARG MODEL_SERVICE_VERSION=0.0.0
ENV MODEL_SERVICE_VERSION=${MODEL_SERVICE_VERSION}
echo $MODEL_SERVICE_VERSION

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV PORT=8080
ENV HOST=0.0.0.0

# Run Flask using flask run
CMD ["flask", "run"]
