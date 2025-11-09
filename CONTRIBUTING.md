# Contributing to Admin Action Bot

Thank you for your interest in contributing to Admin Action Bot! This document provides guidelines for contributing to the project.

## Development Workflow

This project follows strict development protocols using the Admin Action Prompt methodology:

- **Semantic Versioning** (MAJOR.MINOR.PATCH)
- **Comprehensive Logging** - All changes logged in `logs/agent_log.md`
- **PRD-Driven Development** - Features aligned with `docs/PRD.md`
- **Test-First Approach** - All changes must pass tests before version increment

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include:
   - Python version
   - Discord.py version
   - Steps to reproduce
   - Expected vs actual behavior
   - Configuration (sanitized, no tokens!)

### Suggesting Features

1. Check the PRD (`docs/PRD.md`) for planned features
2. Open an issue with the feature request template
3. Explain:
   - Use case
   - Expected behavior
   - Why it fits the project scope

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the development protocol:
   - Update PRD if adding features
   - Write tests for new functionality
   - Update CHANGELOG.md
   - Increment VERSION appropriately
   - Log changes in `logs/agent_log.md`
4. Ensure all tests pass (`python3 -m pytest tests/ -v`)
5. Commit with descriptive messages
6. Push to your fork
7. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/admin-action-bot.git
cd admin-action-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python3 -m pytest tests/ -v

# Copy example config
cp .env.example .env
# Edit .env with your test credentials
```

## Code Standards

- **Python**: Follow PEP 8
- **Type Hints**: Use type hints where applicable
- **Documentation**: Docstrings for all public functions/classes
- **Testing**: Minimum 80% code coverage
- **Commits**: Use conventional commit messages

## Testing

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_config.py -v

# Run with coverage
python3 -m pytest tests/ --cov=src --cov-report=html
```

## Version Increment Guidelines

- **MAJOR (x.0.0)**: Breaking changes, incompatible API changes
- **MINOR (0.x.0)**: New features, backwards-compatible
- **PATCH (0.0.x)**: Bug fixes, documentation updates

## Project Structure

```
admin-action-bot/
├── src/              # Source code
│   ├── bot.py        # Discord bot client
│   ├── config.py     # Configuration management
│   └── __init__.py
├── tests/            # Test suite
├── docs/             # Documentation
│   └── PRD.md        # Product Requirements Document
├── logs/             # Development logs
│   └── agent_log.md  # Complete activity history
├── main.py           # Entry point
├── setup.sh          # Automated setup script
└── requirements.txt  # Python dependencies
```

## Documentation

When adding features:
1. Update `docs/PRD.md` with feature specifications
2. Update `README.md` with usage instructions
3. Update `CHANGELOG.md` with changes
4. Add comments in code for complex logic

## Questions?

- Open an issue for questions
- Check existing documentation in `docs/`
- Review the PRD for project scope and roadmap

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
