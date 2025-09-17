@echo off

echo 🏗️ Building AI Research Agent Docker Images
echo ===========================================

REM Build backend
echo 📦 Building backend image...
cd backend
docker build -t ai-research-backend:latest .
cd ..

REM Build frontend
echo 📦 Building frontend image...
cd frontend-nextjs
docker build -t ai-research-frontend:latest .
cd ..

echo ✅ Build complete!
echo.
echo 🚀 To run with Docker Compose:
echo docker-compose up -d
echo.
echo 🚀 To deploy to Kubernetes:
echo cd k8s ^&^& kubectl apply -f .

pause