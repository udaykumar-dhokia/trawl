# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial release of trawl - On-Premise AI Powered Research Assistant
- Textual TUI interface for interactive research
- FastAPI backend with streaming responses
- Support for Ollama and Google Gemini LLMs
- PostgreSQL with pgvector for document storage
- Web search integration with SearxNG
- Image and video search capabilities
- Persistent chat history
- Source citation system

### Changed

- Restructured project for professional open source standards
- Moved from `src/` to root-level `trawl/` package
- Updated build system to use Hatchling
- Added comprehensive linting and type checking

### Technical

- Added Ruff for code linting and formatting
- Added MyPy for static type checking
- Added proper project metadata and scripts
- Created CLI entry points for different use cases
