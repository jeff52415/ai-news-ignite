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
    graph = build_news_graph(debug=True)
    
    initial_state = {
        "input_message": "Start searching for news about the latest trends in AI and machine learning. Provide maximum 2 articles.",
        "news": None,
        "article": None,
        "results": []
    }
    
    result = await graph.ainvoke(
        initial_state,
        config={"callbacks": [langfuse_handler], "recursion_limit": 200}
    )
    
    # Print results
    print("\nResults:")
    for idx, result in enumerate(result["results"], 1):
        print(f"\n{idx}. {result}")

if __name__ == "__main__":
    asyncio.run(main()) 