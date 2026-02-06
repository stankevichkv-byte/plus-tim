#!/usr/bin/env pwsh
# PowerShell скрипт для развёртывания PlusTim на VPS

$server = "194.67.127.153"
$user = "root"
$repo = "https://github.com/stankevichkv-byte/plus-tim.git"
$projectDir = "/root/plus-tim"

Write-Host "🚀 Начинаем развёртывание PlusTim на $server" -ForegroundColor Green

# Команды для выполнения на сервере
$commands = @"
# Обновление системы
apt-get update && apt-get install -y curl git docker.io docker-compose

# Клонирование репозитория
rm -rf $projectDir
git clone $repo $projectDir
cd $projectDir

# Создание .env файла
cat > .env << 'EOF'
DATABASE_URL=sqlite:///./data/plustim.db
BOT_TOKEN=your_bot_token_here
EOF

# Создание необходимых директорий
mkdir -p data static/audio

# Запуск контейнеров
docker-compose down 2>/dev/null || true
docker-compose up -d --build

# Проверка статуса
docker-compose ps
echo "✅ Развёртывание завершено!"
echo "Backend доступен на http://$server:8000"
"@

# Сохраняем команды во временный файл
$commands | Out-File -Encoding UTF8 temp_deploy.sh

Write-Host "📤 Выполняю команды на сервере..." -ForegroundColor Yellow
& scp -o StrictHostKeyChecking=no temp_deploy.sh ${user}@${server}:/root/
& ssh -o StrictHostKeyChecking=no ${user}@${server} "chmod +x /root/temp_deploy.sh && /root/temp_deploy.sh"

# Очистка
Remove-Item temp_deploy.sh -ErrorAction SilentlyContinue

Write-Host "🎉 Готово!" -ForegroundColor Green