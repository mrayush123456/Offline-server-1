#!/bin/bash

# Stop script on errors
set -e

echo "=== Starting Deployment Process ==="

# Update and install system dependencies
echo "=== Updating System and Installing Dependencies ==="
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv curl nginx git

# Install Poetry if not installed
if ! command -v poetry &> /dev/null
then
    echo "=== Installing Poetry ==="
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "=== Poetry Already Installed ==="
fi

# Clone your Flask app from the repository
echo "=== Cloning Repository ==="
if [ ! -d "flask_instagram_automation" ]; then
    git clone <YOUR_REPO_URL> flask_instagram_automation
else
    cd flask_instagram_automation
    git pull origin main
    cd ..
fi

cd flask_instagram_automation

# Install Python dependencies with Poetry
echo "=== Installing Python Dependencies ==="
poetry install

# Configure Gunicorn (WSGI Server)
echo "=== Configuring Gunicorn ==="
cat > gunicorn_config.py <<EOL
bind = "0.0.0.0:8000"
workers = 4
EOL

# Setup Nginx Configuration
echo "=== Setting Up Nginx ==="
sudo bash -c 'cat > /etc/nginx/sites-available/flask_instagram_automation <<EOL
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL'

sudo ln -sf /etc/nginx/sites-available/flask_instagram_automation /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Run Flask app with Gunicorn using Poetry
echo "=== Starting Flask App ==="
poetry run gunicorn -c gunicorn_config.py app:app --daemon

echo "=== Deployment Complete! ==="
