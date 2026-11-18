# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm

ARG TARGETARCH
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 1. Install minimal system tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    tar \
    gzip \
    && rm -rf /var/lib/apt/lists/*

# 2. Download and bundle matching wireproxy binary for ARM64/AMD64
RUN set -eux; \
    ARCH="${TARGETARCH:-amd64}"; \
    case "${ARCH}" in \
        "arm64"|"aarch64") WP_ARCH="arm64" ;; \
        "amd64"|"x86_64") WP_ARCH="amd64" ;; \
        *) WP_ARCH="amd64" ;; \
    esac; \
    mkdir -p /app/bin; \
    curl -sSL -f "https://github.com/pufferffish/wireproxy/releases/download/v1.0.6/wireproxy_linux_${WP_ARCH}.tar.gz" -o /tmp/wp.tar.gz; \
    tar -xzf /tmp/wp.tar.gz -C /app/bin wireproxy; \
    chmod +x /app/bin/wireproxy; \
    rm -f /tmp/wp.tar.gz

# 3. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy project source code and assets
COPY src/ /app/src/
COPY data/ /app/data/
COPY config.example.yaml run.py /app/

# 5. Create persistent output directories
RUN mkdir -p /app/data /app/results

VOLUME ["/app/data"]

ENTRYPOINT ["python3", "run.py"]
CMD ["--no-dashboard"]
