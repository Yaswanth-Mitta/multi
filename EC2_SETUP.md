# EC2 Manual Setup Guide

## Prerequisites on EC2
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js 16+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Git
sudo apt install git -y
```

## Setup Application
```bash
# Clone repository
git clone https://github.com/Yaswanth-Mitta/multi.git
cd multi

# Switch to prod branch
git checkout prod

# Configure environment
cp .env.example .env
nano .env  # Edit with your API keys and EC2 IP
```

## Configure .env for EC2
```env
# Replace with your actual values
SERP_API_KEY=your_serp_api_key_here
NEWSDATA_API_KEY=your_newsdata_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

# IMPORTANT: Set your EC2 public IP
PUBLIC_IP=your_ec2_public_ip_here
HOST=0.0.0.0
PORT=8000

# Frontend configuration
NEXT_PUBLIC_BACKEND_URL=http://your_ec2_public_ip_here:8000
```

## Start Services
```bash
# Option 1: Use startup script
chmod +x start-manual.sh
./start-manual.sh

# Option 2: Manual start
# Terminal 1 - Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py

# Terminal 2 - Frontend
cd frontend-nextjs
npm install
npm run dev -- --hostname 0.0.0.0
```

## Configure EC2 Security Group
Open these ports in your EC2 security group:
- **Port 3000** (Frontend)
- **Port 8000** (Backend)
- **Port 22** (SSH)

## Access Application
- **Frontend**: http://your_ec2_public_ip:3000
- **Backend API**: http://your_ec2_public_ip:8000

## Production Deployment
```bash
# Frontend production build
cd frontend-nextjs
npm run build
npm start -- --hostname 0.0.0.0 --port 3000

# Backend production
cd backend
source venv/bin/activate
python server.py
```

## Process Management (Optional)
```bash
# Install PM2 for process management
sudo npm install -g pm2

# Start backend with PM2
cd backend
source venv/bin/activate
pm2 start server.py --name "ai-research-backend" --interpreter python

# Start frontend with PM2
cd frontend-nextjs
pm2 start "npm run start" --name "ai-research-frontend"

# Save PM2 configuration
pm2 save
pm2 startup
```

## Troubleshooting
```bash
# Check if services are running
sudo netstat -tlnp | grep :3000
sudo netstat -tlnp | grep :8000

# Check logs
pm2 logs  # If using PM2
tail -f backend/logs/*  # Direct logs

# Test connectivity
curl http://your_ec2_ip:8000/
curl http://your_ec2_ip:3000/
```