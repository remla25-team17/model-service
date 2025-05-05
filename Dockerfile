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

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8080
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask using flask run
CMD ["flask", "run"]
