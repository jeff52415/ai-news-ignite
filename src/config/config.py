from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from pathlib import Path
import yaml
import os

config_path = Path(__file__).parent.parent.parent / "config.yaml"



class ReasoningConfig(BaseModel):
    """Responses API reasoning setting for the research model."""
    effort: Optional[str] = None


class OpenAISearchToolConfig(BaseModel):
    """Hosted web search plus the model that runs the research pass.

    The tool payload sent to OpenAI is only `type`, `search_context_size`,
    and `external_web_access`. `model`, `reasoning`, and `include` are applied
    to the research chat model. `tool_choice` is not forced, because the agent
    still has to return the structured briefing after it finishes searching.
    `return_token_budget` is accepted so the YAML stays valid; the current
    web_search tool has no such field.
    """
    type: str
    search_context_size: Optional[str] = None
    model: Optional[str] = None
    external_web_access: Optional[bool] = None
    return_token_budget: Optional[str] = None
    tool_choice: Optional[str] = None
    include: list[str] = Field(default_factory=list)
    reasoning: Optional[ReasoningConfig] = None

    def as_tool(self) -> Dict[str, Any]:
        tool: Dict[str, Any] = {"type": self.type}
        if self.search_context_size:
            tool["search_context_size"] = self.search_context_size
        if self.external_web_access is not None:
            tool["external_web_access"] = self.external_web_access
        return tool

class AgentConfig(BaseModel):
    name: str
    prompt_key: str
    model: str
    debug: Optional[bool] = False

class AgentsConfig(BaseModel):
    initial_search: AgentConfig
    search_and_summarise: AgentConfig
    github_assistant: AgentConfig
    supervisor: AgentConfig

class ToolGithubConfig(BaseModel):
    docker_image: str
    transport: str

class ToolConfig(BaseModel):
    github: ToolGithubConfig
    openai_search_tools: OpenAISearchToolConfig

class EnvConfig(BaseModel):
    """Configuration for environment variables."""
    openai: Dict[str, str]
    github: Dict[str, str]
    langfuse: Dict[str, str]

    def get_env_value(self, key: str) -> Optional[str]:
        """Get environment value from config, resolving ${VAR} references."""
        if not key.startswith('${') or not key.endswith('}'):
            return key
        env_var = key[2:-1]  # Remove ${ and }
        return os.getenv(env_var)

    def check_required_env_vars(self) -> None:
        """Check if all required environment variables are present."""
        missing_vars = []
        
        # Check OpenAI API key
        if not self.get_env_value(self.openai['api_key']):
            missing_vars.append('OPENAI_API_KEY')
            
        # Check GitHub token
        if not self.get_env_value(self.github['token']):
            missing_vars.append('GIT_PERSONAL_ACCESS_TOKEN')
            
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    def get_langfuse_handler(self) -> Optional[Any]:
        """Get Langfuse handler if all credentials are present."""
        # Check if all required Langfuse environment variables are present
        env_vars = {
            'LANGFUSE_SECRET_KEY': self.langfuse['secret_key'],
            'LANGFUSE_PUBLIC_KEY': self.langfuse['public_key'],
            'LANGFUSE_HOST': self.langfuse['host']
        }
        
        missing_vars = [var for var, value in env_vars.items() 
                       if not self.get_env_value(value)]
        
        if missing_vars:
            return None
            
        from langfuse.langchain import CallbackHandler
        return CallbackHandler()

class AppConfig(BaseModel):
    """Configuration for application settings."""
    input_message: str
    debug: bool = True
    primary_window_days: int = 7
    fallback_window_days: int = 30
    min_findings: int = 5
    max_findings: int = 10

class Config(BaseModel):
    """Main configuration object loaded from YAML."""
    env: EnvConfig
    agents: AgentsConfig
    tool: ToolConfig
    app: AppConfig

    @classmethod
    def load(cls, path: str = config_path) -> "Config":
        """Load config from YAML file."""
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            config = cls.model_validate(data)
            config.env.check_required_env_vars()
            return config
        except FileNotFoundError:
            raise RuntimeError(f"Config file not found: {path}")
        except ValidationError as e:
            raise RuntimeError(f"Config validation error: {e}")


# Example usage:
# config = Config.load()

