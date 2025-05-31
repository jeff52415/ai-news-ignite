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
    env_var_value = os.getenv(github_cfg.env_var_key)
    client = MultiServerMCPClient(
        {
            "github": {
                "command": "docker",
                "args": [
                    "run",
                    "-i",
                    "--rm",
                    "-e",
                    github_cfg.env_var_key,
                    github_cfg.docker_image
                ],
                "env": {
                    github_cfg.env_var_key: env_var_value,
                    **os.environ,
                },
                "transport": github_cfg.transport,
            }
        }
    )
    # Ex. get_file_contents
    if specific_tool:
        tools = await client.get_tools()
        return [tool for tool in tools if tool.name in specific_tool]
    else:
        return await client.get_tools()

# Usage: tools = await get_github_tools()
