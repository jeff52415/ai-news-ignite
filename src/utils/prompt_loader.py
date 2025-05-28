# src/utils/prompt_loader.py
from pathlib import Path
from typing import Dict, List, Any, Set
import logging
from functools import lru_cache
from jinja2 import Environment, FileSystemLoader, Template, TemplateError, meta
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

class PromptError(Exception):
    """Base exception for prompt-related errors."""
    pass

class PromptNotFoundError(PromptError):
    """Raised when a prompt template is not found."""
    pass

class PromptValidationError(PromptError):
    """Raised when prompt validation fails."""
    pass

@dataclass
class PromptTemplate:
    """
    Represents a prompt template with its metadata.
    """
    name: str
    template: Template
    required_variables: Set[str]
    metadata: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)

    def validate_variables(self, provided_vars: Dict[str, Any]) -> None:
        """
        Validate that all required variables are provided.
        Raises PromptValidationError if any required variable is missing.
        """
        missing = self.required_variables - set(provided_vars.keys())
        if missing:
            raise PromptValidationError(
                f"Missing required variables for prompt {self.name}: {missing}"
            )

class PromptLoader:
    """
    Production-ready prompt loader with Jinja2 templating support.
    Loads, validates, and renders prompt templates from the prompts directory.
    """
    
    def __init__(self):
        self._prompts: Dict[str, PromptTemplate] = {}
        self._setup_logging()
        self._setup_jinja()
        self._preload_all_prompts()
    
    def _setup_logging(self):
        """
        Configure logging for the prompt loader.
        """
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def _setup_jinja(self):
        """
        Setup Jinja2 environment. Autoescape only for HTML files.
        """
        project_root = Path(__file__).parent.parent.parent
        prompts_dir = project_root / "prompts"
        self.env = Environment(
            loader=FileSystemLoader(str(prompts_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=self._select_autoescape
        )

    @staticmethod
    def _select_autoescape(template_name):
        """
        Enable autoescaping only for HTML files.
        """
        if template_name is None:
            return False
        return template_name.endswith(('.html', '.htm'))

    def _extract_required_variables(self, template: Template) -> Set[str]:
        """
        Extract required variables from a Jinja2 template using jinja2.meta.
        """
        try:
            source = template.environment.loader.get_source(template.environment, template.name)[0]
            parsed_content = template.environment.parse(source)
            variables = meta.find_undeclared_variables(parsed_content)
            return set(variables)
        except Exception as e:
            logger.warning(f"Failed to extract variables from template '{template.name}': {e}")
            return set()

    def _preload_all_prompts(self):
        """
        Preload all Jinja2 prompt templates from the prompts directory.
        """
        try:
            templates = self.env.list_templates()
            for name in templates:
                if name.endswith('.j2'):
                    try:
                        template = self.env.get_template(name)
                        required_vars = self._extract_required_variables(template)
                        self._prompts[name[:-3]] = PromptTemplate(
                            name=name[:-3],
                            template=template,
                            required_variables=required_vars,
                            metadata={
                                "version": "1.0",  # Could be loaded from a separate file
                                "description": f"Template for {name[:-3]}",
                                "created_at": datetime.now().isoformat()
                            }
                        )
                        logger.info(f"Preloaded prompt: {name}")
                    except TemplateError as e:
                        logger.error(f"Failed to load template {name}: {e}")
        except Exception as e:
            logger.error(f"Failed to preload prompts: {e}")

    @lru_cache(maxsize=32)
    def get_prompt(self, name: str) -> PromptTemplate:
        """
        Get a prompt template by name.
        Raises PromptNotFoundError if not found.
        """
        if name not in self._prompts:
            raise PromptNotFoundError(f"Prompt template not found: {name}")
        return self._prompts[name]

    def format_prompt(self, name: str, **kwargs) -> str:
        """
        Format a prompt template with the provided variables.
        Args:
            name: Name of the prompt template
            **kwargs: Variables to substitute in the template
        Returns:
            Formatted prompt string
        Raises:
            PromptValidationError: If required variables are missing
            PromptError: If template rendering fails
        """
        try:
            prompt = self.get_prompt(name)
            prompt.validate_variables(kwargs)
            return prompt.template.render(**kwargs)
        except TemplateError as e:
            raise PromptError(f"Failed to render template {name}: {str(e)}")
        except Exception as e:
            raise PromptError(f"Failed to format prompt {name}: {str(e)}")

    def list_prompts(self) -> List[str]:
        """
        Return a list of all available prompt names.
        """
        return list(self._prompts.keys())

    def get_prompt_metadata(self, name: str) -> Dict[str, Any]:
        """
        Get metadata for a specific prompt.
        """
        prompt = self.get_prompt(name)
        return {
            "name": prompt.name,
            "required_variables": list(prompt.required_variables),
            "metadata": prompt.metadata,
            "created_at": prompt.created_at.isoformat()
        }

# Create a singleton instance
prompt_loader = PromptLoader()