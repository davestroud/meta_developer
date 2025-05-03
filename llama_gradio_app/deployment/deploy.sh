#!/bin/bash

# Exit on error
set -e

# Variables
APP_NAME="llama_gradio_app"
DOMAIN="ishtar-ai.com"
APP_DIR="/var/www/${DOMAIN}/${APP_NAME}"
VENV_DIR="/var/www/${DOMAIN}/venv"
NGINX_CONF="/etc/nginx/sites-available/${DOMAIN}.conf"
SYSTEMD_SERVICE="/etc/systemd/system/gradio-app.service"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting deployment of ${APP_NAME} to ${DOMAIN}...${NC}"

# Check if running as root
if [ "$(id -u)" != "0" ]; then
   echo -e "${RED}This script must be run as root${NC}" 
   exit 1
fi

# Create directory structure
echo -e "${GREEN}Creating directory structure...${NC}"
mkdir -p /var/www/${DOMAIN}

# Copy application files
echo -e "${GREEN}Copying application files...${NC}"
cp -r ../ ${APP_DIR}

# Set up Python virtual environment
echo -e "${GREEN}Setting up Python virtual environment...${NC}"
python3 -m venv ${VENV_DIR}
source ${VENV_DIR}/bin/activate
pip install --upgrade pip
pip install -r ${APP_DIR}/requirements.txt
pip install gunicorn uvicorn

# Set proper permissions
echo -e "${GREEN}Setting proper permissions...${NC}"
chown -R www-data:www-data /var/www/${DOMAIN}
chmod -R 755 /var/www/${DOMAIN}

# Install and configure Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    echo -e "${GREEN}Installing Nginx...${NC}"
    apt-get update
    apt-get install -y nginx
fi

# Configure Nginx
echo -e "${GREEN}Configuring Nginx...${NC}"
cp ${APP_DIR}/deployment/ishtar-ai.com.conf ${NGINX_CONF}
ln -sf ${NGINX_CONF} /etc/nginx/sites-enabled/

# Check Nginx configuration
echo -e "${GREEN}Checking Nginx configuration...${NC}"
nginx -t

# Set up systemd service
echo -e "${GREEN}Setting up systemd service...${NC}"
cp ${APP_DIR}/deployment/gradio-app.service ${SYSTEMD_SERVICE}

# Restart services
echo -e "${GREEN}Restarting services...${NC}"
systemctl daemon-reload
systemctl enable gradio-app
systemctl restart gradio-app
systemctl restart nginx

# Set up SSL with Certbot if not already set up
if [ ! -d "/etc/letsencrypt/live/${DOMAIN}" ]; then
    echo -e "${GREEN}Setting up SSL with Certbot...${NC}"
    if ! command -v certbot &> /dev/null; then
        apt-get update
        apt-get install -y certbot python3-certbot-nginx
    fi
    certbot --nginx -d ${DOMAIN} -d www.${DOMAIN} --non-interactive --agree-tos --email admin@${DOMAIN}
    systemctl restart nginx
fi

echo -e "${GREEN}Deployment complete! Your Gradio app should now be available at https://${DOMAIN}${NC}"
echo -e "${GREEN}Check the status of the application with: systemctl status gradio-app${NC}"
echo -e "${GREEN}View logs with: journalctl -u gradio-app${NC}" 