# AI News Ignite 🤖📰

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LangGraph](https://img.shields.io/badge/LangGraph-Enabled-orange.svg)](https://github.com/langchain-ai/langgraph)

> Automated collection and summarization of the latest AI news using LangGraph agents and GitHub Actions.

## ✨ Features

- 🤖 Automated AI news collection and summarization using LangGraph
- 📰 Continuously updated news articles in the `news` folder

## 🔄 Flow

The system follows a LangGraph-based workflow:

1. **Search News** - Fetch latest AI/ML news articles
2. **Filter News** - Remove duplicate and irrelevant articles
3. **Map Articles** - Process each article in parallel
4. **Summarize & Publish** - Generate summaries and prepare for publication
5. **Collect Results** - Aggregate all processed articles

All processed news articles are automatically saved in the `news` folder, which is continuously updated through GitHub Actions.

## 🚀 Setup

1. **Clone** the repository
   ```bash
   git clone https://github.com/yourusername/ai-news-ignite.git
   cd ai-news-ignite
   ```

2. **Configure** environment variables:
   
   You can configure the required variables either through:
   - Local `.env` file for development
   - GitHub repository secrets for automated runs

   Required variables:
   ```bash
   # Required
   OPENAI_API_KEY=your_openai_key
   GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token

   # Optional - for monitoring
   LANGFUSE_SECRET_KEY=your_langfuse_secret
   LANGFUSE_PUBLIC_KEY=your_langfuse_public
   LANGFUSE_HOST=your_langfuse_host
   ```

3. **Install** dependencies:
   ```bash
   uv sync
   ```

4. **Run** the application:
   ```bash
   uv run python app.py
   ```

## ⚙️ Configuration

All configuration settings are managed in `config.yaml`. The system includes regular updates via GitHub Actions.

## 📊 Monitoring

With Langfuse integration (optional), you can track all operations and performance metrics through the Langfuse dashboard.

---

<div align="center">
Made with ❤️ by AI News Ignite Team
</div>
