# TCG Pokemon Decks Project

A Python project for building and managing Pokemon TCG decks. This is a monorepo consisting of the data ETL, backend, and frontend development towards a UI for managing trading cards.

## Prerequisites

- Python 3.9 or higher
- Poetry (dependency manager)

## Installation

### 1. Install Poetry
```bash
# Using Homebrew (macOS)
brew install poetry
```

### 2. Clone and Setup
```bash
git clone <your-repo-url>
cd tcg-poke-decks
```

### 3. Install Dependencies
```zsh
poetry install
```

This will:
- Create a virtual environment automatically
- Install all dependencies from `pyproject.toml`
- Install both main and development dependencies

## Virtual Environment Management

### Poetry 2.0+ (New Way)
```zsh
# Create and activate virtual environment
poetry env use python
source $(poetry env info --path)/bin/activate

# Deactivate when done
deactivate
```

## Running the Project

```zsh
# Check Python version in Poetry environment
poetry run python --version
# Detailed environment information
poetry env info
# Python executable Poetry is using
```


### Method 1: Direct Execution (Recommended)
```zsh
# Run Python files directly
poetry run python src/data/extract.py

# Run Python commands
poetry run python -c "import requests; print('requests works!')"
```

### Method 2: Activated Environment
```zsh
# Activate the environment first
source $(poetry env info --path)/bin/activate

# Then run normally
python src/data/extract.py

# Deactivate when done
deactivate
```

## Pre-commit Hooks

### Setup
```zsh
# Install pre-commit as a dev dependency
poetry add --group dev pre-commit

# Install the pre-commit hooks
poetry run pre-commit install
```

### Running Pre-commit Hooks
```zsh
# Run all hooks on all files
poetry run pre-commit run --all-files

# Run all hooks on staged files only
poetry run pre-commit run

# Run a specific hook
poetry run pre-commit run black --all-files
poetry run pre-commit run isort --all-files
poetry run pre-commit run flake8 --all-files
```

### What Happens
Every time you commit, pre-commit automatically:
- Formats your code with Black
- Sorts your imports with isort
- Checks for linting issues with flake8
- Only allows the commit if all checks pass