# trawl - On-Premise AI Powered Research Assistant

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Textual](https://img.shields.io/badge/Built%20with-Textual-ff00ff.svg)](https://textual.textualize.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**trawl** is a high-performance, On-Premise AI Powered Research Assistant with terminal interface. Inspired by modern search assistants like Perplexity, it brings deep-dive research capabilities directly to your command line.

![trawl Demo Mockup](./demo.svg)

---

## Features

- **Live Streaming Responses**: Real-time markdown streaming for immediate feedback
- **Visual Research Insights**: Dedicated image and video sidebar displaying relevant visuals discovered during research
- **Smart Research Orchestration**: Automatically searches the web, processes multiple sources, and synthesizes answers
- **Source Citations**: Interactive sidebar displaying all research sources with site-specific icons/emojis
- **Persistent Threads**: Full chat history support powered by PostgreSQL and SQLAlchemy
- **Premium TUI**: A sleek, customizable terminal interface with both Light and Dark themes
- **Fast-API Backend**: Robust, asynchronous backend architecture for multi-step research
- **Multiple LLM Support**: Integration with Google Gemini and Ollama
- **Vector Search**: pgvector-powered semantic search for efficient document retrieval

---

## Technology Stack

- **Frontend**: [Textual](https://textual.textualize.io/) (Rich TUI Framework)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous Python Web Framework)
- **Database**: [PostgreSQL](https://www.postgresql.org/) with [pgvector](https://github.com/pgvector/pgvector) and [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **LLM Engine**: Integration with Google Gemini / Ollama
- **Search Engine**: [SearxNG](https://github.com/searxng/searxng)
- **Embeddings**: [Sentence Transformers](https://www.sbert.net/)

---

## Quick Start

### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) package manager
- PostgreSQL database
- SearxNG instance (optional, for web search)
- Ollama (optional, for local LLM support)

### Installation

```bash
# Clone the repository
git clone https://github.com/udaykumar-dhokia/trawl.git
cd trawl

# Install dependencies
uv sync

# Or for development
uv sync --dev
```

### Configuration

1. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:

   ```bash
   # Database
   DATABASE_URL=postgresql://user:password@localhost:5432/trawl_db

   # API
   API_BASE=http://localhost:8000

   # Search Engine
   SEARXNG_BASE_URL=http://localhost:8888

   # LLM Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   GOOGLE_API_KEY=your_api_key_here
   LLM_PROVIDER=ollama  # or 'google'
   ```

### Database Setup

1. Create a PostgreSQL database
2. Install pgvector extension:
   ```sql
   CREATE EXTENSION vector;
   ```
3. Run the initial migration (if available) or the app will create tables automatically

### Usage

#### Terminal User Interface (Recommended)

```bash
# Start the interactive TUI
trawl --tui

# Or using make
make tui
```

#### Command Line Query

```bash
# Single query mode
trawl --query "What is quantum computing?"

# Or using make
make query QUERY="What is quantum computing?"
```

#### API Server

```bash
# Start the FastAPI server
trawl

# Or run directly
uv run trawl
```

#### Programmatic Usage

```python
import asyncio
from trawl.services.invoke_chat import invoke_chat

async def main():
    await invoke_chat(query="Your research question here")

asyncio.run(main())
```

---

## Development

### Setup Development Environment

```bash
# Run the development setup script
./scripts/setup-dev.sh

# Or manually
uv sync --dev
cp .env.example .env
```

### Running Tests

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov=trawl

# Run specific test
uv run pytest tests/test_specific.py
```

### Code Quality

```bash
# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Type checking
uv run mypy .
```

### Building

```bash
# Build package
uv build

# Or using make
make build
```

---

## Project Structure

```
trawl/
├── cli.py              # Command-line interface
├── main.py             # FastAPI application
├── tui_app.py          # Textual TUI interface
├── core/               # Core configuration and utilities
├── db/                 # Database models and connections
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic schemas
├── services/           # Business logic services
└── utils/              # Utility functions

tests/                  # Test suite
docs/                   # Documentation
examples/               # Usage examples
scripts/                # Development scripts
.github/                # GitHub Actions and templates
```

---

## Docker

Build and run with Docker:

```bash
# Build image
docker build -t trawl .

# Run container
docker run -p 8000:8000 --env-file .env trawl
```

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## Support

- 📖 [Documentation](https://github.com/udaykumar-dhokia/trawl#readme)
- 🐛 [Issues](https://github.com/udaykumar-dhokia/trawl/issues)
- 💬 [Discussions](https://github.com/udaykumar-dhokia/trawl/discussions)

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/trawl_db
SEARXNG_BASE_URL=http://localhost:8080
GOOGLE_API_KEY=your_gemini_api_key
DEFAULT_MODEL=gemini-1.5-pro
API_BASE=http://localhost:8000
```

### 4. Running the Application

#### Option A: Using Docker Compose (Recommended)

This will start everything (Database, SearXNG, Redis, and Backend) automatically.

```bash
docker compose up -d
```

Once the containers are up, launch the Research TUI:

```bash
uv run python src/tui_app.py
```

#### Option B: Manual Startup

Launch the FastAPI backend:

```bash
uv run fastapi run src/main.py
```

Launch the Research TUI:

```bash
uv run python src/tui_app.py
```

---

## Keyboard Shortcuts

| Shortcut   | Action            |
| :--------- | :---------------- |
| `Ctrl + N` | New Chat          |
| `Ctrl + R` | Refresh Chat List |
| `Escape`   | Blur / Exit Input |
| `Ctrl + C` | Quit Application  |

---

## 🤝 Contributing

Contributions are welcome! Whether it's adding a new search provider, improving the UI, or fixing bugs, please feel free to fork the repo and submit a PR.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<p align="center">Built with ❤️ by udthedeveloper</p>
