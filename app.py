import asyncio
from dotenv import load_dotenv
from pathlib import Path
from config.config import Config
from agent.graph import build_news_graph

# Load environment variables
PROJECT_ROOT = Path(__file__).parent
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)

async def main():
    # Load configuration
    config = Config.load()
    langfuse_handler = config.env.get_langfuse_handler()
    
    # Build and execute graph
    graph = build_news_graph(debug=config.app.debug)
    
    initial_state = {
        "input_message": config.app.input_message,
        "news": None,
        "article": None,
        "results": []
    }
    
    callbacks = [langfuse_handler] if langfuse_handler else []
    result = await graph.ainvoke(
        initial_state,
        config={"callbacks": callbacks, "recursion_limit": 200}
    )
    
    # Print results
    print("\nAI Technical Intelligence Briefing")
    findings = result["results"]
    if not findings:
        print("\nNo developments met the selection criteria in this window.")
    for idx, finding in enumerate(findings, 1):
        print(f"\n{idx}. {finding}")

if __name__ == "__main__":
    asyncio.run(main()) 