# src/agent/agents.py
"""
Agent definitions for the AI News Ignite project.
Includes:
- AgentFactory: provides async access to all agents
"""
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from config.config import Config
from utils.prompt_loader import prompt_loader
from agent.tools.link import is_valid_link
from data_model.news import NewsArticleList
from data_model.summarise_agent import SummariseAgentResponse
from agent.tools.github_tool import get_github_tools
from agent.tools.date import get_current_date
from langgraph.graph.state import CompiledStateGraph
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel

# Set the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)

# Load config
config = Config.load()

class AgentFactory:
    """Factory for creating and accessing all agents asynchronously."""
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.supervisor = None
        self._agent_cfg = config.agents

    @staticmethod
    def list_agents():
        """Return a list of available agent names."""
        return list(config.agents.model_dump().keys())
    
    async def get_initial_search_agent(self, response_format: BaseModel = NewsArticleList) -> CompiledStateGraph:
        agent_cfg = self._agent_cfg.initial_search
        search_tool = {
            "type": config.tool.openai_search_tools.type,
            "search_context_size": config.tool.openai_search_tools.search_context_size,
        }
        initial_search_prompt = await prompt_loader.get_prompt(agent_cfg.prompt_key).template.render_async()
        if self.verbose:
            print(f"Initial search prompt: {initial_search_prompt}")
        initial_search_agent = create_react_agent(
            model=agent_cfg.model,
            tools=[get_current_date, search_tool],
            debug=agent_cfg.debug,
            prompt=initial_search_prompt,
            name=agent_cfg.name,
            response_format=response_format,
        )
        return initial_search_agent

    async def get_search_and_summarise_agent(self, response_format: BaseModel = SummariseAgentResponse) -> CompiledStateGraph:
        agent_cfg = self._agent_cfg.search_and_summarise
        summary_prompt = prompt_loader.get_prompt(agent_cfg.prompt_key)
        summarised_prompt = await summary_prompt.template.render_async()
        search_tool = {
            "type": config.tool.openai_search_tools.type,
            "search_context_size": config.tool.openai_search_tools.search_context_size,
        }
        if self.verbose:
            print(f"Search and summarise prompt: {summarised_prompt}")
            print(f"Response format: {response_format}")
        search_and_summarise_agent = create_react_agent(
            model=agent_cfg.model,
            tools=[is_valid_link, search_tool],
            debug=agent_cfg.debug,
            prompt=summarised_prompt,
            name=agent_cfg.name,
            response_format=response_format,  # Could be made dynamic if needed
        )
        return search_and_summarise_agent

    async def get_github_assistant(self, specific_tool: list[str] | None = None, response_format: BaseModel = None) -> CompiledStateGraph:
        agent_cfg = self._agent_cfg.github_assistant
        tools = await get_github_tools(specific_tool)
        github_agent_prompt = await prompt_loader.get_prompt(agent_cfg.prompt_key).template.render_async()
        if self.verbose:
            print(f"Github assistant prompt: {github_agent_prompt}")
            print(f"Response format: {response_format}")
            print(f"Tools: {tools}")
        github_assistant = create_react_agent(
            model=agent_cfg.model,
            tools=tools,
            debug=agent_cfg.debug,
            prompt=github_agent_prompt,
            name=agent_cfg.name,
            response_format=response_format,
        )
        return github_assistant

    async def get_supervisor(self) -> CompiledStateGraph:
        if self.supervisor is None:
            from langgraph_supervisor import create_supervisor
            agent_cfg = self._agent_cfg.supervisor
            search_and_summarise_agent = await self.get_search_and_summarise_agent(response_format=None)
            github_assistant = await self.get_github_assistant()
            supervisor_prompt = await prompt_loader.get_prompt(agent_cfg.prompt_key).template.render_async()
            if self.verbose:
                print(f"Supervisor prompt: {supervisor_prompt}")
            self.supervisor = create_supervisor(
                agents=[search_and_summarise_agent, github_assistant],
                model=ChatOpenAI(model=agent_cfg.model),
                prompt=supervisor_prompt,
            ).compile()
        return self.supervisor

# Usage:
# factory = AgentFactory()
# search_agent = await factory.get_search_and_summarise_agent()
# github_agent = await factory.get_github_assistant()
# supervisor = await factory.get_supervisor()
# available_agents = AgentFactory.list_agents() 