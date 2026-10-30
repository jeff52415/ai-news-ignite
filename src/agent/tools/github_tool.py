import os
from typing import List, Any
from config.config import Config

# Optional: for MCP GitHub agent
async def get_github_tools(specific_tool: list[str] | None = None) -> List[Any]:
    """Async function to get GitHub tools from MCP server."""
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
    except ImportError:
        raise ImportError("langchain_mcp_adapters is required for the GitHub agent.")
    
    config = Config.load()
    github_cfg = config.tool.github
    github_token = config.env.get_env_value(config.env.github['token'])
    
    if not github_token:
        raise EnvironmentError("GitHub token not found in environment variables")
    
    client = MultiServerMCPClient(
        {
            "github": {
                "command": "docker",
                "args": [
                    "run",
                    "-i",
                    "--rm",
                    "-e",
                    "GITHUB_PERSONAL_ACCESS_TOKEN",
                    github_cfg.docker_image
                ],
                "env": {
                    **os.environ,
                    # Set after os.environ so an empty host variable cannot wipe the token.
                    "GITHUB_PERSONAL_ACCESS_TOKEN": github_token,
                    "GH_TOKEN": github_token,
                    "GITHUB_TOKEN": github_token,
                },
                "transport": github_cfg.transport,
            }
        }
    )
    # Ex. get_file_contents
    tools = await client.get_tools()
    if specific_tool:
        tools = [tool for tool in tools if tool.name in specific_tool]
    return [_guard_tool(tool) for tool in tools]


def _guard_tool(tool):
    """Turn a GitHub 404 into a tool result instead of killing the graph.

    A missing news/YYYY-MM path is normal. The MCP client raises McpError for
    that response, and LangGraph treats it as a failed task.
    """
    notice = (
        "GitHub tool failed: {exc}. A 404 means that path is not on the branch yet. "
        "Create the file directly instead of reading the missing path again."
    )
    returns_artifact = getattr(tool, "response_format", None) == "content_and_artifact"

    def _failure(exc: Exception):
        message = notice.format(exc=exc)
        if returns_artifact:
            return message, None
        return message

    if getattr(tool, "coroutine", None) is not None:
        original = tool.coroutine

        async def coroutine(*args, _original=original, **kwargs):
            try:
                return await _original(*args, **kwargs)
            except Exception as exc:
                return _failure(exc)

        tool.coroutine = coroutine
    if getattr(tool, "func", None) is not None:
        original_func = tool.func

        def func(*args, _original=original_func, **kwargs):
            try:
                return _original(*args, **kwargs)
            except Exception as exc:
                return _failure(exc)

        tool.func = func
    return tool

# Usage: tools = await get_github_tools()
