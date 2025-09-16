from typing import Dict, Any, Optional
import json
from datetime import datetime

class MemoryService:
    def __init__(self):
        self.current_session = None
        self.research_data = {}
        self.conversation_history = []
    
    def start_new_session(self, product_name: str, research_data: Dict[str, Any]):
        """Start a new research session with scraped data"""
        self.current_session = {
            'product': product_name,
            'timestamp': datetime.now().isoformat(),
            'research_complete': True
        }
        self.research_data = research_data
        self.conversation_history = []
        print(f"\n🧠 Memory: Started new session for '{product_name}'")
    
    def add_conversation(self, query: str, response: str):
        """Add conversation to memory"""
        self.conversation_history.append({
            'query': query,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    def has_active_session(self) -> bool:
        """Check if there's an active research session"""
        return self.current_session is not None and self.current_session.get('research_complete', False)
    
    def get_research_context(self) -> str:
        """Get the research data as context for follow-up questions"""
        if not self.research_data:
            return ""
        
        context = f"PREVIOUS RESEARCH DATA FOR {self.current_session['product']}:\n\n"
        
        # Add web content
        if 'web_content' in self.research_data:
            context += "=== WEB REVIEWS ===\n"
            context += self.research_data['web_content'][:1500] + "\n\n"
        
        # Add YouTube content
        if 'youtube_content' in self.research_data:
            context += "=== YOUTUBE REVIEWS ===\n"
            context += self.research_data['youtube_content'][:1000] + "\n\n"
        
        # Add Reddit content
        if 'reddit_content' in self.research_data:
            context += "=== REDDIT DISCUSSIONS ===\n"
            context += self.research_data['reddit_content'][:800] + "\n\n"
        
        # Add conversation history
        if self.conversation_history:
            context += "=== PREVIOUS CONVERSATION ===\n"
            for conv in self.conversation_history[-3:]:  # Last 3 exchanges
                context += f"Q: {conv['query']}\nA: {conv['response'][:200]}...\n\n"
        
        return context
    
    def clear_session(self):
        """Clear current session"""
        if self.current_session:
            print(f"\n🧠 Memory: Cleared session for '{self.current_session['product']}'")
        self.current_session = None
        self.research_data = {}
        self.conversation_history = []
    
    def get_session_info(self) -> Optional[Dict[str, Any]]:
        """Get current session info"""
        return self.current_session