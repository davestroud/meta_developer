# Deploying to ishtar-ai.com

This guide explains how to deploy the Llama Gradio App to ishtar-ai.com.

## Prerequisites

- A server running Ubuntu 20.04 or later (or similar Debian-based distribution)
- SSH access to the server with root or sudo privileges
- Domain (ishtar-ai.com) pointed to your server's IP address in DNS settings
- Python 3.11+ installed on the server

## Deployment Options

### Option 1: Docker Deployment (Easiest)

Docker is the simplest way to deploy your application as it handles all dependencies and environment setup automatically.

1. Copy the entire project directory to your server:
   ```bash
   rsync -avz --exclude 'venv' --exclude '*.pyc' --exclude '__pycache__' --exclude '.git' ./llama_gradio_app user@your-server:/tmp/
   ```

2. SSH into your server:
   ```bash
   ssh user@your-server
   ```

3. Move the app to its permanent location:
   ```bash
   sudo mkdir -p /var/www/ishtar-ai.com
   sudo cp -r /tmp/llama_gradio_app /var/www/ishtar-ai.com/
   cd /var/www/ishtar-ai.com/llama_gradio_app
   ```

4. Create a .env file with your API key:
   ```bash
   sudo nano .env
   ```
   
   Add:
   ```
   LLAMA_API_KEY=your_api_key_here
   ```

5. Run the Docker deployment script:
   ```bash
   sudo ./deployment/docker_deploy.sh
   ```

6. Your app will be available at https://ishtar-ai.com

### Option 2: Traditional Web Server Deployment

1. Copy the entire project directory to your server:
   ```bash
   rsync -avz --exclude 'venv' --exclude '*.pyc' --exclude '__pycache__' --exclude '.git' ./llama_gradio_app user@your-server:/tmp/
   ```

2. SSH into your server:
   ```bash
   ssh user@your-server
   ```

3. Navigate to the deployment directory and run the deployment script:
   ```bash
   cd /tmp/llama_gradio_app/deployment
   sudo ./deploy.sh
   ```

4. Follow the on-screen prompts if any.

### Option 3: Manual Deployment

If you prefer to do a manual deployment or the automated script doesn't work for your setup:

1. Install required packages:
   ```bash
   sudo apt update
   sudo apt install -y python3-venv python3-pip nginx
   ```

2. Set up directory structure:
   ```bash
   sudo mkdir -p /var/www/ishtar-ai.com
   ```

3. Copy application files:
   ```bash
   sudo cp -r /tmp/llama_gradio_app /var/www/ishtar-ai.com/
   ```

4. Set up virtual environment:
   ```bash
   sudo python3 -m venv /var/www/ishtar-ai.com/venv
   sudo /var/www/ishtar-ai.com/venv/bin/pip install --upgrade pip
   sudo /var/www/ishtar-ai.com/venv/bin/pip install -r /var/www/ishtar-ai.com/llama_gradio_app/requirements.txt
   sudo /var/www/ishtar-ai.com/venv/bin/pip install gunicorn uvicorn
   ```

5. Set proper permissions:
   ```bash
   sudo chown -R www-data:www-data /var/www/ishtar-ai.com
   sudo chmod -R 755 /var/www/ishtar-ai.com
   ```

6. Set up Nginx:
   ```bash
   sudo cp /var/www/ishtar-ai.com/llama_gradio_app/deployment/ishtar-ai.com.conf /etc/nginx/sites-available/
   sudo ln -s /etc/nginx/sites-available/ishtar-ai.com.conf /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. Set up systemd service:
   ```bash
   sudo cp /var/www/ishtar-ai.com/llama_gradio_app/deployment/gradio-app.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable gradio-app
   sudo systemctl start gradio-app
   ```

8. Set up SSL with Certbot:
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d ishtar-ai.com -d www.ishtar-ai.com
   ```

## Verification and Troubleshooting

### For Docker deployment:
```bash
# Check if containers are running
docker ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart
```

### For traditional deployment:
```bash
# Check service status
sudo systemctl status gradio-app

# View application logs
sudo journalctl -u gradio-app

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Testing the configuration:
```bash
curl -I https://ishtar-ai.com
```

## Environment Variables

Make sure to set up your `.env` file with the required API keys:
```bash
sudo nano /var/www/ishtar-ai.com/llama_gradio_app/.env
```

Add your Llama API key:
```
LLAMA_API_KEY=your_llama_api_key_here
```

## Updates

### For Docker deployment:
```bash
# Copy updated files
rsync -avz --exclude 'venv' --exclude '*.pyc' --exclude '__pycache__' --exclude '.git' ./llama_gradio_app user@your-server:/tmp/

# Update files
sudo cp -r /tmp/llama_gradio_app/* /var/www/ishtar-ai.com/llama_gradio_app/

# Rebuild and restart containers
cd /var/www/ishtar-ai.com/llama_gradio_app
docker-compose down
docker-compose build
docker-compose up -d
```

### For traditional deployment:
```bash
# Copy updated files
rsync -avz --exclude 'venv' --exclude '*.pyc' --exclude '__pycache__' --exclude '.git' ./llama_gradio_app user@your-server:/tmp/

# Update files
sudo cp -r /tmp/llama_gradio_app/* /var/www/ishtar-ai.com/llama_gradio_app/
sudo chown -R www-data:www-data /var/www/ishtar-ai.com
sudo systemctl restart gradio-app
``` 