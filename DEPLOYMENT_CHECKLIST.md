# EC2 Deployment Checklist

## 1. EC2 Security Group Configuration
Ensure your EC2 security group allows:
```
- Port 8000 (HTTP) - Source: 0.0.0.0/0
- Port 22 (SSH) - Source: Your IP
```

## 2. Deploy and Start Application
```bash
# On your EC2 instance:
chmod +x ec2-setup.sh
./ec2-setup.sh
```

## 3. Access URLs
Replace `YOUR_EC2_IP` with your actual EC2 public IP:

- **Frontend**: `http://YOUR_EC2_IP:8000`
- **API Status**: `http://YOUR_EC2_IP:8000/status`
- **Health Check**: `http://YOUR_EC2_IP:8000/memory-status`

## 4. Test from Your Browser
1. Open `http://YOUR_EC2_IP:8000` in your browser
2. You should see the AI Research Agent interface
3. Try example queries:
   - "iPhone 15 Pro review"
   - "Tesla stock analysis"
   - "Samsung Galaxy S24 vs iPhone 15"

## 5. Troubleshooting
If you can't access from browser:

```bash
# Check if service is running
sudo netstat -tuln | grep :8000

# Check EC2 security group
aws ec2 describe-security-groups --group-ids YOUR_SG_ID

# Check application logs
tail -f /var/log/syslog | grep python
```

## 6. Features Available
- ✅ Web interface accessible from any browser
- ✅ Real-time product analysis
- ✅ Stock market data
- ✅ YouTube video analysis
- ✅ Conversational memory
- ✅ Mobile-friendly design
- ✅ Demo mode if APIs not configured