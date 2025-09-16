class ResearchAgentUI {
    constructor() {
        this.apiUrl = 'http://localhost:8000';
        this.currentSession = null;
        this.conversationHistory = [];
        this.outputMode = 'terminal'; // 'terminal' or 'report'
        this.backendAvailable = false;
        
        this.initializeElements();
        this.bindEvents();
        this.checkSystemStatus();
    }

    initializeElements() {
        // Input elements
        this.queryInput = document.getElementById('queryInput');
        this.submitBtn = document.getElementById('submitBtn');
        this.clearBtn = document.getElementById('clearBtn');
        
        // Memory elements
        this.memoryStatus = document.getElementById('memoryStatus');
        this.memoryText = document.getElementById('memoryText');
        this.clearMemoryBtn = document.getElementById('clearMemoryBtn');
        
        // Results elements
        this.loadingState = document.getElementById('loadingState');
        this.resultsContainer = document.getElementById('resultsContainer');
        this.resultTitle = document.getElementById('resultTitle');
        this.resultAgent = document.getElementById('resultAgent');
        this.resultTime = document.getElementById('resultTime');
        this.resultContent = document.getElementById('resultContent');
        
        // Conversation elements
        this.conversationHistory = document.getElementById('conversationHistory');
        this.conversationList = document.getElementById('conversationList');
        
        // Mode selection elements
        this.terminalModeBtn = document.getElementById('terminalModeBtn');
        this.reportModeBtn = document.getElementById('reportModeBtn');
        
        // Status elements
        this.backendStatus = document.getElementById('backendStatus');
        this.awsStatus = document.getElementById('awsStatus');
        this.googleStatus = document.getElementById('googleStatus');
        this.newsStatus = document.getElementById('newsStatus');
        
        // Loading steps
        this.loadingSteps = {
            step1: document.getElementById('step1'),
            step2: document.getElementById('step2'),
            step3: document.getElementById('step3'),
            step4: document.getElementById('step4'),
            step5: document.getElementById('step5')
        };
    }

    bindEvents() {
        // Submit button
        this.submitBtn.addEventListener('click', () => this.handleSubmit());
        
        // Enter key in textarea
        this.queryInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSubmit();
            }
        });
        
        // Clear button
        this.clearBtn.addEventListener('click', () => this.clearInput());
        
        // Clear memory button
        this.clearMemoryBtn.addEventListener('click', () => this.clearMemory());
        
        // Mode selection buttons
        this.terminalModeBtn.addEventListener('click', () => this.setOutputMode('terminal'));
        this.reportModeBtn.addEventListener('click', () => this.setOutputMode('report'));
        
        // Example query buttons
        document.querySelectorAll('.example-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const query = btn.getAttribute('data-query');
                this.queryInput.value = query;
                this.handleSubmit();
            });
        });
    }

    setOutputMode(mode) {
        this.outputMode = mode;
        
        // Update button states
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        if (mode === 'terminal') {
            this.terminalModeBtn.classList.add('active');
        } else {
            this.reportModeBtn.classList.add('active');
        }
    }

    async checkSystemStatus() {
        try {
            const response = await fetch(`${this.apiUrl}/status`);
            if (response.ok) {
                const status = await response.json();
                this.backendAvailable = true;
                this.updateSystemStatus({
                    backend: true,
                    ...status
                });
            } else {
                this.backendAvailable = false;
                this.updateSystemStatus({
                    backend: false,
                    aws: false,
                    google: false,
                    news: false
                });
            }
        } catch (error) {
            console.log('Backend not running, using demo mode');
            this.backendAvailable = false;
            this.updateSystemStatus({
                backend: false,
                aws: false,
                google: false,
                news: false
            });
        }
    }

    updateSystemStatus(status) {
        this.backendStatus.textContent = status.backend ? '🟢 Connected' : '🔴 Demo Mode';
        this.awsStatus.textContent = status.aws ? '🟢 Connected' : '🔴 Offline';
        this.googleStatus.textContent = status.google ? '🟢 Connected' : '🔴 Offline';
        this.newsStatus.textContent = status.news ? '🟢 Active' : '🟡 Disabled';
    }

    async handleSubmit() {
        const query = this.queryInput.value.trim();
        if (!query) return;

        this.showLoading();
        this.hideResults();

        try {
            // Simulate loading steps
            await this.simulateLoadingSteps();
            
            // Make API call
            const response = await fetch(`${this.apiUrl}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query })
            });

            if (response.ok) {
                const result = await response.json();
                this.displayResults(result, query);
                this.updateMemoryStatus(result.session);
            } else {
                // Demo mode - generate mock response
                const mockResult = this.generateMockResponse(query);
                this.displayResults(mockResult, query);
            }
        } catch (error) {
            console.log('Using demo mode');
            const mockResult = this.generateMockResponse(query);
            this.displayResults(mockResult, query);
        }

        this.hideLoading();
    }

    async simulateLoadingSteps() {
        const steps = ['step1', 'step2', 'step3', 'step4', 'step5'];
        
        for (let i = 0; i < steps.length; i++) {
            // Remove active class from all steps
            Object.values(this.loadingSteps).forEach(step => {
                step.classList.remove('active');
            });
            
            // Add active class to current step
            this.loadingSteps[steps[i]].classList.add('active');
            
            // Wait before next step
            await new Promise(resolve => setTimeout(resolve, 800));
        }
    }

    generateMockResponse(query) {
        const queryLower = query.toLowerCase();
        let agent = 'GENERAL';
        let analysis = '';

        // Determine agent type
        if (queryLower.includes('stock') || queryLower.includes('tesla') || queryLower.includes('nvidia')) {
            agent = 'NEWS';
            analysis = `
╔══════════════════════════════════════════════════════════════════════════════╗
║                     COMPREHENSIVE STOCK ANALYSIS                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: ${query}

📊 REAL-TIME STOCK DATA:
┌─────────────────────────────────────────────────────────────────┐
│  Tesla Inc (TSLA)                                               │
└─────────────────────────────────────────────────────────────────┘

💰 CURRENT TRADING SESSION:
   ├─ Current Price: $248.50
   ├─ Change: $+12.30 (+5.20%)
   ├─ Today's Open: $236.20
   ├─ Day Range: $235.10 - $249.80
   └─ Volume: 45,230,000

📈 COMPREHENSIVE ANALYSIS:
Based on the real-time stock data, Tesla shows strong bullish momentum with:

1. **Current Performance**: +5.20% gain indicates positive market sentiment
2. **Technical Analysis**: Breaking above key resistance levels
3. **Market Position**: Leading EV manufacturer with strong fundamentals
4. **Investment Recommendation**: BUY - Strong growth potential
5. **Risk Factors**: Market volatility, regulatory changes
6. **Price Target**: $275-$300 (12-month outlook)

═══════════════════════════════════════════════════════════════════════════════
Real-time Stock Data + News Analysis | Yahoo Finance + AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════`;
        } else if (queryLower.includes('pixel') || queryLower.includes('iphone') || queryLower.includes('samsung') || queryLower.includes('review')) {
            agent = 'PRODUCT';
            analysis = `
╔══════════════════════════════════════════════════════════════════════════════╗
║                        PRODUCT MARKET ANALYSIS                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: ${query}
🏷️  CATEGORY: PRODUCT

📊 MARKET ANALYSIS:
**Product Overview**: Premium smartphone with advanced AI capabilities, exceptional camera system, and flagship performance.

**Performance Analysis**: 
- Tensor G4 processor delivers excellent performance for daily tasks
- 12GB RAM ensures smooth multitasking
- Battery life: 24+ hours with adaptive battery management

**User Experience**: 
- 10 YouTube reviews analyzed show 85% positive sentiment
- Users praise camera quality and software optimization
- Minor concerns about charging speed compared to competitors

**Pros & Cons**:
✅ Exceptional camera with AI enhancements
✅ Clean Android experience with 7 years updates
✅ Premium build quality and design
❌ Charging speed slower than competitors
❌ Limited storage options
❌ Price premium over similar specs

🎯 PURCHASE ASSESSMENT:
**Overall Score**: 8.5/10 based on comprehensive review analysis

**Target Buyers**: Photography enthusiasts, Android purists, users wanting long-term software support

**Use Case Scenarios**: 
- Professional photography and content creation
- Business users needing reliable performance
- Users prioritizing software updates and security

**Final Recommendation**: STRONG BUY - Excellent value for photography-focused users. Wait for sales if budget-conscious.

💬 CONVERSATIONAL MODE ACTIVATED
→ Ask follow-up questions about this product (colors, price, specs, etc.)
→ Type 'exit' to start fresh research

═══════════════════════════════════════════════════════════════════════════════
Product Analysis + Conversational Mode | Search Data + AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════`;
        } else {
            analysis = `
╔══════════════════════════════════════════════════════════════════════════════╗
║                           GENERAL ANALYSIS                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: ${query}

📝 ANALYSIS:
Based on comprehensive research and analysis, here are the key insights:

**Market Overview**: The query relates to current market trends and consumer interests in technology and innovation sectors.

**Key Findings**:
1. **Market Demand**: High consumer interest in the specified area
2. **Competitive Landscape**: Multiple players with varying value propositions
3. **Technology Trends**: Rapid advancement driving consumer adoption
4. **Price Sensitivity**: Consumers balancing features vs cost

**Recommendations**:
- Consider timing for optimal value
- Compare multiple options before deciding
- Factor in long-term value and support
- Monitor market developments for better deals

**Risk Assessment**: Moderate risk with good potential for satisfaction based on current market conditions.

═══════════════════════════════════════════════════════════════════════════════
General Analysis | AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════`;
        }

        return {
            result: analysis,
            agent: agent,
            timestamp: new Date().toISOString(),
            session: queryLower.includes('review') || queryLower.includes('pixel') || queryLower.includes('iphone') ? {
                active: true,
                product: query.split(' ').slice(0, 2).join(' ')
            } : null
        };
    }

    displayResults(result, query) {
        this.resultTitle.textContent = `Analysis Results`;
        this.resultAgent.textContent = `${result.agent} Agent`;
        this.resultTime.textContent = new Date(result.timestamp).toLocaleString();
        
        // Format output based on selected mode
        if (this.outputMode === 'report') {
            this.resultContent.innerHTML = this.formatCleanReport(result.result);
        } else {
            this.resultContent.innerHTML = `<pre>${result.result}</pre>`;
        }
        
        this.showResults();
        
        // Add to conversation history if it's a follow-up
        if (this.currentSession) {
            this.addToConversationHistory(query, result.result);
        }
    }

    updateMemoryStatus(session) {
        if (session && session.active) {
            this.currentSession = session;
            this.memoryText.textContent = `Active session: ${session.product}`;
            this.memoryStatus.classList.remove('hidden');
            this.conversationHistory.classList.remove('hidden');
        } else {
            this.currentSession = null;
            this.memoryStatus.classList.add('hidden');
            this.conversationHistory.classList.add('hidden');
        }
    }

    addToConversationHistory(query, response) {
        const conversationItem = document.createElement('div');
        conversationItem.className = 'conversation-item';
        conversationItem.innerHTML = `
            <div class="conversation-query">Q: ${query}</div>
            <div class="conversation-response">A: ${response.substring(0, 200)}...</div>
        `;
        this.conversationList.appendChild(conversationItem);
    }

    clearMemory() {
        this.currentSession = null;
        this.memoryStatus.classList.add('hidden');
        this.conversationHistory.classList.add('hidden');
        this.conversationList.innerHTML = '';
        
        // Call API to clear memory
        fetch(`${this.apiUrl}/clear-memory`, { method: 'POST' })
            .catch(() => console.log('Demo mode - memory cleared locally'));
    }

    formatCleanReport(rawResult) {
        // Extract content between analysis sections
        let cleanContent = rawResult
            .replace(/[╔═╗║╚╝┌─┐│└┘]/g, '') // Remove box drawing characters
            .replace(/={3,}/g, '') // Remove separator lines
            .replace(/\n\s*\n/g, '\n') // Remove extra blank lines
            .trim();
        
        // Convert to HTML with better formatting
        cleanContent = cleanContent
            .replace(/📋 QUERY: (.+)/g, '<h3>🔍 Query</h3><p>$1</p>')
            .replace(/📊 (.+?):/g, '<h4>📊 $1</h4>')
            .replace(/🎯 (.+?):/g, '<h4>🎯 $1</h4>')
            .replace(/📈 (.+?):/g, '<h4>📈 $1</h4>')
            .replace(/💬 (.+?):/g, '<h4>💬 $1</h4>')
            .replace(/\n/g, '<br>');
        
        return `<div class="clean-report">${cleanContent}</div>`;
    }

    clearInput() {
        this.queryInput.value = '';
        this.queryInput.focus();
    }

    showLoading() {
        this.loadingState.classList.remove('hidden');
        this.submitBtn.disabled = true;
        this.submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    }

    hideLoading() {
        this.loadingState.classList.add('hidden');
        this.submitBtn.disabled = false;
        this.submitBtn.innerHTML = '<i class="fas fa-search"></i> Analyze';
    }

    showResults() {
        this.resultsContainer.classList.remove('hidden');
    }

    hideResults() {
        this.resultsContainer.classList.add('hidden');
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new ResearchAgentUI();
});