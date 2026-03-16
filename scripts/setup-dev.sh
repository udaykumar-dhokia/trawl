#!/usr/bin/env bash
# Development setup script for trawl

set -e

echo "🚀 Setting up trawl development environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if Python 3.10+ is available
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "❌ Python 3.10 or higher is required"
    exit 1
fi

echo "📦 Installing dependencies..."
uv sync

echo "🔧 Setting up pre-commit hooks..."
# Add pre-commit setup here if needed

echo "📋 Copying environment template..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "   Please edit .env with your configuration"
else
    echo "ℹ️  .env file already exists"
fi

echo "🧪 Running initial checks..."
uv run ruff check .
uv run mypy .

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your configuration"
echo "2. Start PostgreSQL and other services"
echo "3. Run 'make tui' to start the interface"
echo "4. Run 'make test' to run tests"