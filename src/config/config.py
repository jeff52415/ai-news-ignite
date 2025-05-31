from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from pathlib import Path
import yaml

config_path = Path(__file__).parent.parent.parent / "config.yaml"



class OpenAISearchToolConfig(BaseModel):
    """Configuration for a tool, extensible for extra fields."""
    type: str
    search_context_size: Optional[str] = None
    model: Optional[str] = None
    extra: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("extra")
    def collect_extra(cls, values):
        allowed = {"type", "search_context_size", "model"}
        extra = {k: v for k, v in values.items() if k not in allowed}
        values["extra"] = extra
        return values

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
    env_var_key: str
    transport: str

class ToolConfig(BaseModel):
    github: ToolGithubConfig
    openai_search_tools: OpenAISearchToolConfig

class Config(BaseModel):
    """Main configuration object loaded from YAML."""
    agents: AgentsConfig
    tool: ToolConfig
    # Add more fields for other services as needed

    @classmethod
    def load(cls, path: str = config_path) -> "Config":
        """Load config from YAML file."""
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            return cls.model_validate(data)
        except FileNotFoundError:
            raise RuntimeError(f"Config file not found: {path}")
        except ValidationError as e:
            raise RuntimeError(f"Config validation error: {e}")


# Example usage:
# config = Config.load()

