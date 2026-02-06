FROM python:3.11-slim-bookworm

WORKDIR /app

# Disable default Debian mirrors and use Russian mirror
RUN rm -f /etc/apt/sources.list.d/*.list 2>/dev/null; \
    echo 'deb http://mirror.yandex.ru/debian bookworm main contrib non-free' > /etc/apt/sources.list && \
    echo 'deb http://mirror.yandex.ru/debian-security bookworm-security main contrib non-free' >> /etc/apt/sources.list

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application with gunicorn for production
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]