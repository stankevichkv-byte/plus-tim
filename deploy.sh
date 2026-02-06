#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting deployment...${NC}"

# Variables
SERVER_IP="YOUR_SERVER_IP"
SERVER_USER="root"
APP_DIR="/root/plus-tim"

# Check if git remote exists
if ! git remote get-url origin &>/dev/null; then
    echo -e "${YELLOW}Adding git remote...${NC}"
    git remote add origin git@github.com:stankevichkv-byte/plus-tim.git
fi

# Pull latest code from GitHub
echo -e "${GREEN}Pulling latest code from GitHub...${NC}"
git pull origin main

# Build and start Docker containers
echo -e "${GREEN}Building Docker container...${NC}"
docker-compose build

echo -e "${GREEN}Stopping old container...${NC}"
docker-compose down

echo -e "${GREEN}Starting new container...${NC}"
docker-compose up -d

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${GREEN}API available at: http://localhost:8000${NC}"

# Restart nginx
echo -e "${YELLOW}Reloading nginx...${NC}"
docker-compose exec nginx nginx -s reload