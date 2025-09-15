# Clean Architecture - Multi-Agent LLM System

## Architecture Overview

This system implements a clean architecture using three main design patterns:

### 1. Orchestrator (Mediator Pattern)
- **File**: `orchestrator.py`
- **Role**: Central brain controlling the workflow
- **Responsibilities**:
  - Query classification using LLM
  - Agent selection and routing
  - Error handling and logging
  - Does NOT instantiate agents directly

### 2. Factory Pattern
- **File**: `factory.py`
- **Role**: Agent creation and management
- **Responsibilities**:
  - Creates agent instances by type
  - Manages agent lifecycle
  - Easily extensible for new agents

### 3. Agent Interface
- **File**: `interfaces.py`
- **Role**: Standard contract for all agents
- **Methods**:
  - `process(query, context)`: Main processing method
  - `get_agent_type()`: Returns agent type identifier

## Current Agents

### NewsAgent (`agents/news_agent.py`)
- Handles NEWS and STOCKS queries
- Uses NewsData.io API for real-time data
- Provides market sentiment analysis

### ProductAgent (`agents/product_agent.py`)
- Handles PRODUCT queries
- Uses Google Search for product data
- Provides market analysis and purchase likelihood

### GeneralAgent (`agents/general_agent.py`)
- Handles GENERAL queries
- Uses LLM for comprehensive analysis

### ValidatorAgent (`agents/validator_agent.py`)
- Example of extensibility
- Validates information accuracy
- Demonstrates how to add new agents

## Adding New Agents

1. **Create Agent Class**:
   ```python
   from ..interfaces import Agent
   
   class MyNewAgent(Agent):
       def process(self, query: str, context: Dict[str, Any] = None) -> str:
           # Implementation
           pass
       
       def get_agent_type(self) -> str:
           return "MY_NEW_TYPE"
   ```

2. **Update Factory**:
   ```python
   # In factory.py _create_agent method
   elif agent_type == "MY_NEW_TYPE":
       return MyNewAgent(self.llm_service)
   ```

3. **Update Classification** (if needed):
   ```python
   # In orchestrator.py classify_query method
   # Add new classification logic
   ```

## Benefits

- **Separation of Concerns**: Each component has a single responsibility
- **Extensibility**: Easy to add new agents without modifying existing code
- **Testability**: Each component can be tested independently
- **Maintainability**: Clean interfaces and minimal coupling
- **Scalability**: Factory pattern allows for efficient agent management