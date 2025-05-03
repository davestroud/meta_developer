#!/bin/bash

# Exit on error
set -e

# Variables
DOMAIN="ishtar-ai.com"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Docker deployment for ${DOMAIN}...${NC}"

# Check if running as root
if [ "$(id -u)" != "0" ]; then
   echo -e "${RED}This script must be run as root${NC}" 
   exit 1
fi

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
    echo -e "${GREEN}Installing Docker...${NC}"
    apt-get update
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt-get update
    apt-get install -y docker-ce
fi

# Install Docker Compose if not already installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}Installing Docker Compose...${NC}"
    curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Set up SSL with Certbot
if [ ! -d "/etc/letsencrypt/live/${DOMAIN}" ]; then
    echo -e "${GREEN}Setting up SSL with Certbot...${NC}"
    apt-get update
    apt-get install -y certbot
    certbot certonly --standalone -d ${DOMAIN} -d www.${DOMAIN} --non-interactive --agree-tos --email admin@${DOMAIN}
fi

# Create directories
echo -e "${GREEN}Creating directories...${NC}"
mkdir -p static tmp

# Set proper permissions
echo -e "${GREEN}Setting proper permissions...${NC}"
chown -R 1000:1000 .

# Deploy with Docker Compose
echo -e "${GREEN}Deploying with Docker Compose...${NC}"
docker-compose build
docker-compose up -d

echo -e "${GREEN}Deployment complete! Your Gradio app should now be available at https://${DOMAIN}${NC}"
echo -e "${GREEN}View logs with: docker-compose logs -f${NC}" 