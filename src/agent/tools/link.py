import requests
from urllib.parse import urlparse
from requests.exceptions import RequestException
from langchain_core.tools import tool, InjectedToolArg
from pydantic import BaseModel, Field
from typing import Annotated


class LinkToolInput(BaseModel):
    url: str | list[str] = Field(description="The URL to check")
    timeout: Annotated[int, InjectedToolArg] = Field(description="Timeout in seconds for the request", default=5)

@tool(name_or_callable="is_valid_link", parse_docstring=False, args_schema=LinkToolInput)
def is_valid_link(url: str | list[str], timeout: int = 5) -> dict | list[dict]:
    """
    Check if a URL is valid and accessible.
    
    Args:
        url (str | list[str]): The URL to check
        timeout (int): Timeout in seconds for the request
        
    Returns:
        dict | list[dict]: {"url_link": ..., "valid": bool} for each URL
    """
    def check_single(u: str) -> dict:
        try:
            result = urlparse(u)
            if not all([result.scheme, result.netloc]):
                return {"url_link": u, "valid": False}
            response = requests.head(u, timeout=timeout, allow_redirects=True)
            return {"url_link": u, "valid": response.status_code < 400}
        except RequestException:
            return {"url_link": u, "valid": False}
        except Exception:
            return {"url_link": u, "valid": False}

    if isinstance(url, str):
        return check_single(url)
    elif isinstance(url, list):
        return [check_single(u) for u in url]