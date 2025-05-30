from pydantic import BaseModel, Field, field_validator


class SummariseAgentResponse(BaseModel):
    """
    Response model for summarisation agent output.
    Attributes:
        file_name (str): A concise markdown file name (must end with .md, e.g., 'gpt-4o-mini-release.md').
        markdown_file (str): The markdown content, following correct markdown format.
    """
    file_name: str = Field(
        description="A concise markdown file name (e.g., 'gpt-4o-mini-release.md'). Must end with .md."
    )
    markdown_file: str = Field(
        description="The markdown file content, following correct markdown format."
    )

    @field_validator("file_name")
    @classmethod
    def validate_file_name(cls, v: str) -> str:
        if not v.endswith(".md"):
            raise ValueError("The file_name must end with '.md'. Example: 'gpt-4o-mini-release.md'.")
        return v