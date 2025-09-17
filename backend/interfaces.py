from abc import ABC, abstractmethod
from typing import Dict, Any

class Agent(ABC):
    """Standard interface that all agents must implement"""
    
    @abstractmethod
    def process(self, query: str, context: Dict[str, Any] = None) -> str:
        """Process a query and return results"""
        pass
    
    @abstractmethod
    def get_agent_type(self) -> str:
        """Return the type/name of this agent"""
        pass