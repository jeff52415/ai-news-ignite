from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from pathlib import Path
import yaml

config_path = Path(__file__).parent / "config.yaml"

class OpenAIModelConfig(BaseModel):
    """Configuration for the main GPT model."""
    name: str
    temperature: float = 0.2

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

class Config(BaseModel):
    """Main configuration object loaded from YAML."""
    gpt_model: OpenAIModelConfig
    openai_search_tools: OpenAISearchToolConfig
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

