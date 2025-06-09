# Stage 1: Builder
FROM python:3 AS builder
RUN echo "Building the Python environment"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --target=/tmp/deps -r requirements.txt

# Stage 2: Final image
FROM python:3-slim AS final
RUN echo "Creating the final image"

WORKDIR /app

# Copy packages and app
COPY --from=builder /tmp/deps /app/deps
COPY src/ /app/

ENV PYTHONPATH="/app/deps"

ENTRYPOINT ["python"]
CMD ["main.py"]