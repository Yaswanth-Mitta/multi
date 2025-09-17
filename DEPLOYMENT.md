# AI Research Agent - Deployment Guide

## 🐳 Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- `.env` file configured with API keys

### Quick Start
```bash
# Build images
./build.sh  # Linux/Mac
# or
build.bat   # Windows

# Start services
docker-compose up -d

# Access
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
```

### Configuration
Update `.env` file:
```env
PUBLIC_IP=your_server_ip
SERP_API_KEY=your_serp_api_key
NEWSDATA_API_KEY=your_newsdata_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

## ☸️ Kubernetes Deployment

### Prerequisites
- Kubernetes cluster running
- kubectl configured
- Docker images built and available

### Deploy to Kubernetes
```bash
# Build images first
./build.sh

# Deploy to cluster
cd k8s
kubectl apply -f .

# Check status
kubectl get pods -n ai-research-agent
kubectl get services -n ai-research-agent
```

### Access Services
- **Frontend**: `http://<node-ip>:30300`
- **Backend**: `http://<node-ip>:30800`

### Update Configuration
Edit `k8s/configmap.yaml` and update secrets:
```bash
kubectl apply -f configmap.yaml
kubectl rollout restart deployment -n ai-research-agent
```

## 🔧 Environment Variables

### Required
- `SERP_API_KEY` - SERP API key
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key

### Optional
- `NEWSDATA_API_KEY` - NewsData.io API key
- `TAVILY_API_KEY` - Tavily AI API key
- `GOOGLE_API_KEY` - Google API key
- `GOOGLE_CSE_ID` - Google CSE ID
- `PUBLIC_IP` - Server public IP (default: localhost)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)

## 📊 Monitoring

### Docker
```bash
# View logs
docker-compose logs -f

# Check health
docker-compose ps
```

### Kubernetes
```bash
# View logs
kubectl logs -f deployment/ai-research-backend -n ai-research-agent
kubectl logs -f deployment/ai-research-frontend -n ai-research-agent

# Check health
kubectl get pods -n ai-research-agent
kubectl describe pod <pod-name> -n ai-research-agent
```

## 🔄 Updates

### Docker
```bash
# Rebuild and restart
./build.sh
docker-compose up -d --build
```

### Kubernetes
```bash
# Rebuild images
./build.sh

# Update deployment
kubectl rollout restart deployment -n ai-research-agent
```

## 🛠️ Troubleshooting

### Common Issues

1. **Backend not accessible**
   - Check `PUBLIC_IP` in `.env`
   - Verify port 8000 is open
   - Check Docker/K8s service status

2. **Frontend can't connect to backend**
   - Update `NEXT_PUBLIC_BACKEND_URL`
   - Check network connectivity
   - Verify backend health endpoint

3. **API errors**
   - Verify API keys in secrets
   - Check rate limits
   - Review backend logs

### Debug Commands
```bash
# Docker
docker-compose exec backend python -c "from config import Config; print(Config.validate_config())"

# Kubernetes
kubectl exec -it deployment/ai-research-backend -n ai-research-agent -- python -c "from config import Config; print(Config.validate_config())"
```