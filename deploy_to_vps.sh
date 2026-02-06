#!/bin/bash
# Bash скрипт для развёртывания PlusTim на VPS (запустить в Git Bash)

SERVER="root@194.67.127.153"
PROJECT_DIR="/root/plus-tim"
REPO="https://github.com/stankevichkv-byte/plus-tim.git"

echo "🚀 Начинаем развёртывание PlusTim на $SERVER"

ssh -o StrictHostKeyChecking=no $SERVER "export REPO='$REPO' && export PROJECT_DIR='$PROJECT_DIR' && bash -s" << 'EOF'
# Обновление и установка Docker
apt-get update -qq 2>/dev/null || true
apt-get install -y -qq curl git 2>/dev/null || true

# Установка Docker Compose (v2)
mkdir -p /usr/local/libexec
curl -SL https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64 -o /usr/local/libexec/docker-compose
chmod +x /usr/local/libexec/docker-compose
ln -sf /usr/local/libexec/docker-compose /usr/local/bin/docker-compose

# Запуск Docker daemon
service docker start 2>/dev/null || dockerd &>/dev/null &
sleep 3

# Остановка старых контейнеров
cd $PROJECT_DIR 2>/dev/null && docker compose down || true

# Клонирование/обновление репозитория
rm -rf $PROJECT_DIR
git clone $REPO $PROJECT_DIR
cd $PROJECT_DIR

# Создание .env файла
cat > .env << 'ENVEOF'
DATABASE_URL=sqlite:///./data/plustim.db
BOT_TOKEN=your_bot_token_here
ENVEOF

# Создание директорий
mkdir -p data static/audio

# Сборка и запуск
docker compose up -d --build

# Проверка
docker compose ps
echo "✅ Развёртывание завершено!"
EOF

echo "🎉 Готово!"