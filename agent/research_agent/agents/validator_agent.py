from typing import Dict, Any
from ..interfaces import Agent
from ..llm_service import LLMService

class ValidatorAgent(Agent):
    """Example of how to add new agents - validates information accuracy"""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    def process(self, query: str, context: Dict[str, Any] = None) -> str:
        validation_prompt = f"""
        Validate the accuracy and reliability of information related to: "{query}"
        
        Provide:
        1. Fact-checking assessment
        2. Source reliability analysis
        3. Potential biases or limitations
        4. Confidence score (0-100%)
        """
        
        validation = self.llm_service.query_llm(validation_prompt)
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        INFORMATION VALIDATION                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: {query}

✅ VALIDATION ANALYSIS:
{validation}

═══════════════════════════════════════════════════════════════════════════════
Validation Analysis | AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════
        """.strip()
    
    def get_agent_type(self) -> str:
        return "VALIDATOR"