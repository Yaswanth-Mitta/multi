#!/bin/bash

# EC2 Deployment Script for AI Research Agent
echo "🚀 Deploying AI Research Agent on EC2"
echo "====================================="

# Get EC2 public IP (replace with your actual IP)
export EC2_PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "YOUR_EC2_IP")

echo "🌐 EC2 Public IP: $EC2_PUBLIC_IP"

# Update security group ports (run these AWS CLI commands if needed)
echo "📋 Required Security Group Rules:"
echo "   • Port 8000 (HTTP) - 0.0.0.0/0"
echo "   • Port 22 (SSH) - Your IP"
echo "   • Port 80 (HTTP) - 0.0.0.0/0 (optional)"
echo "   • Port 443 (HTTPS) - 0.0.0.0/0 (optional)"

# Start the application
echo ""
echo "🚀 Starting application..."
./start-all.sh

echo ""
echo "🌐 Access URLs:"
echo "   Frontend: http://$EC2_PUBLIC_IP:8000"
echo "   API Status: http://$EC2_PUBLIC_IP:8000/status"
echo "   Memory Status: http://$EC2_PUBLIC_IP:8000/memory-status"