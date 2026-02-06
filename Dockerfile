FROM python:3.11-slim-bookworm

WORKDIR /app

# Use Russian mirror - completely replace apt sources
RUN rm -rf /etc/apt/sources.list.d/*.sources /etc/apt/sources.list.d/*.list 2>/dev/null || true
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until
RUN echo 'deb http://mirror.yandex.ru/debian bookworm main contrib non-free' > /etc/apt/sources.list && \
    echo 'deb http://mirror.yandex.ru/debian-security bookworm-security main contrib non-free' >> /etc/apt/sources.list

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configure pip to use timeout and retries
RUN pip config set global.timeout 60 && \
    pip config set global.retries 10 && \
    pip config set global.index-url https://pypi.org/simple && \
    pip config set global.trusted-host pypi.org

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application with gunicorn for production
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]