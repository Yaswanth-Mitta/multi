# Research Agent Web Interface

Modern web frontend for the AI Research Orchestrator with real-time analysis capabilities.

## Features

🎨 **Modern UI Design**
- Glassmorphism design with gradient backgrounds
- Responsive layout for desktop and mobile
- Real-time loading animations
- Interactive agent status indicators

🤖 **Multi-Agent Integration**
- Product Agent for comprehensive product analysis
- News Agent for stock market analysis
- General Agent for versatile queries
- Validator Agent for information verification

💬 **Conversational Interface**
- Memory-based follow-up questions
- Session management for continuous research
- Conversation history tracking
- Smart query classification

📊 **Real-time Features**
- Live system status monitoring
- Progressive loading with step indicators
- Dynamic result formatting
- Auto-refresh capabilities

## Quick Start

### 1. Install Dependencies
```bash
cd frontend
pip install -r requirements.txt
```

### 2. Start the Web Server
```bash
python app.py
```

### 3. Open Browser
Navigate to: `http://localhost:8000`

## Usage

### Example Queries
- **Product Analysis**: "Google Pixel 9 review analysis"
- **Stock Analysis**: "Tesla stock market analysis" 
- **Comparisons**: "iPhone 15 vs Samsung Galaxy S24"
- **Investment**: "NVIDIA stock investment analysis"

### Follow-up Questions
After initial analysis, ask follow-up questions like:
- "What about the camera quality?"
- "How's the battery life?"
- "What are the color options?"
- "Is it worth the price?"

### Memory Management
- System remembers your current research session
- Ask related questions without re-analyzing
- Click "New Research" to start fresh analysis
- Conversation history is maintained per session

## API Endpoints

### Core Endpoints
- `GET /` - Main web interface
- `POST /analyze` - Process user queries
- `GET /status` - System status check
- `POST /clear-memory` - Clear conversation memory

### Request Format
```json
{
  "query": "Google Pixel 9 review analysis"
}
```

### Response Format
```json
{
  "result": "Comprehensive analysis...",
  "agent": "PRODUCT",
  "timestamp": "2024-01-01T12:00:00",
  "session": {
    "active": true,
    "product": "Google Pixel 9"
  }
}
```

## Architecture

### Frontend Stack
- **HTML5** - Semantic structure
- **CSS3** - Modern styling with glassmorphism
- **Vanilla JavaScript** - No framework dependencies
- **Font Awesome** - Icon library

### Backend Integration
- **Flask** - Lightweight web server
- **CORS** - Cross-origin resource sharing
- **Research Agent** - Core analysis engine

### Design Patterns
- **Progressive Enhancement** - Works without JavaScript
- **Responsive Design** - Mobile-first approach
- **Error Handling** - Graceful degradation
- **Demo Mode** - Works without backend

## Customization

### Styling
Edit `styles.css` to customize:
- Color schemes and gradients
- Layout and spacing
- Animation timings
- Responsive breakpoints

### Functionality
Modify `script.js` to add:
- New query examples
- Custom loading messages
- Additional API endpoints
- Enhanced error handling

### Backend
Update `app.py` to:
- Add new API routes
- Modify response formats
- Implement caching
- Add authentication

## Deployment

### Local Development
```bash
python app.py
# Access: http://localhost:8000
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Using Docker
docker build -t research-agent-ui .
docker run -p 8000:8000 research-agent-ui
```

### Environment Variables
```bash
FLASK_ENV=production
FLASK_DEBUG=False
PORT=8000
```

## Browser Support

✅ **Modern Browsers**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

⚠️ **Limited Support**
- Internet Explorer (basic functionality)
- Older mobile browsers

## Performance

- **Initial Load**: < 2 seconds
- **Query Processing**: 5-15 seconds
- **Memory Usage**: < 50MB
- **Mobile Optimized**: Touch-friendly interface

## Security

- CORS protection enabled
- Input validation and sanitization
- No sensitive data in frontend
- API rate limiting ready

## Troubleshooting

### Common Issues

**Backend Not Starting**
```bash
# Check Python path
python --version
# Install missing dependencies
pip install -r requirements.txt
```

**API Connection Failed**
- Verify backend is running on port 8000
- Check firewall settings
- Ensure CORS is properly configured

**Slow Response Times**
- Check AWS Bedrock API limits
- Verify internet connection
- Monitor system resources

### Debug Mode
Enable debug logging:
```bash
FLASK_DEBUG=True python app.py
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## License

MIT License - see LICENSE file for details