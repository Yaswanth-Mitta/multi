from typing import Dict, Any
from ..interfaces import Agent
from ..llm_service import LLMService

class GeneralAgent(Agent):
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    def process(self, query: str, context: Dict[str, Any] = None) -> str:
        general_prompt = f"""
        Provide a comprehensive analysis for: "{query}"
        
        Include relevant insights, recommendations, and actionable information.
        """
        
        analysis = self.llm_service.query_llm(general_prompt)
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           GENERAL ANALYSIS                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: {query}

📝 ANALYSIS:
{analysis}

═══════════════════════════════════════════════════════════════════════════════
General Analysis | AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════
        """.strip()
    
    def get_agent_type(self) -> str:
        return "GENERAL"