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
                    "GITHUB_PERSONAL_ACCESS_TOKEN": github_token,
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
