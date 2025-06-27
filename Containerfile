FROM python:3.11-slim
WORKDIR /app
# Install system dependencies, including ping (iputils-ping) and psql client (postgresql-client)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    iputils-ping \
    postgresql-client \
    net-tools \
    procps \
    curl \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
### test
