from typing import Dict
from .interfaces import Agent
from .agents.news_agent import NewsAgent
from .agents.product_agent import ProductAgent
from .agents.general_agent import GeneralAgent
from .agents.validator_agent import ValidatorAgent
from .news_service import NewsService
from .search_service import SearchService
from .llm_service import LLMService

class AgentFactory:
    def __init__(self, news_service: NewsService, search_service: SearchService, llm_service: LLMService):
        self.news_service = news_service
        self.search_service = search_service
        self.llm_service = llm_service
        self._agents: Dict[str, Agent] = {}
    
    def get_agent(self, agent_type: str) -> Agent:
        """Get or create an agent by type"""
        if agent_type not in self._agents:
            self._agents[agent_type] = self._create_agent(agent_type)
        return self._agents[agent_type]
    
    def _create_agent(self, agent_type: str) -> Agent:
        """Create a new agent instance"""
        if agent_type in ["NEWS", "STOCKS"]:
            return NewsAgent(self.news_service, self.llm_service)
        elif agent_type == "PRODUCT":
            return ProductAgent(self.search_service, self.llm_service)
        elif agent_type == "GENERAL":
            return GeneralAgent(self.llm_service)
        elif agent_type == "VALIDATOR":
            return ValidatorAgent(self.llm_service)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    
    def get_available_agents(self) -> list:
        """Return list of available agent types"""
        return ["NEWS", "STOCKS", "PRODUCT", "GENERAL", "VALIDATOR"]