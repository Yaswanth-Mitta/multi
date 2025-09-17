# Manual Setup Guide

## Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Git (optional)

## Step 1: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
SERP_API_KEY=your_serp_api_key_here
NEWSDATA_API_KEY=your_newsdata_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
PUBLIC_IP=localhost
```

## Step 2: Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python server.py
```

Backend will run on: http://localhost:8000

## Step 3: Frontend Setup (New Terminal)
```bash
# Navigate to frontend
cd frontend-nextjs

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: http://localhost:3000

## Step 4: Access Application
- Open browser: http://localhost:3000
- Backend API: http://localhost:8000

## Production Build (Optional)
```bash
# Frontend production build
cd frontend-nextjs
npm run build
npm start
```

## Troubleshooting

### Backend Issues
```bash
# Check Python version
python --version

# Test backend directly
curl http://localhost:8000/

# Check dependencies
pip list
```

### Frontend Issues
```bash
# Check Node version
node --version

# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues
- Verify `.env` file is in root directory
- Check `PUBLIC_IP` setting in `.env`
- Ensure backend is running before starting frontend