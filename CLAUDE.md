# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tradefun is a vibecoding project that combines trading strategies with bank integrations. The project is in early stages with a modular Python architecture designed for trading strategy development and execution.

## Development Environment

**Python Version**: Requires Python >= 3.12

**Dependency Management**: Uses Poetry for dependency management
- `poetry install` - Install dependencies
- `poetry shell` - Activate virtual environment
- `poetry add <package>` - Add new dependency
- `poetry add --group dev <package>` - Add development dependency

**Environment Setup**: The `scripts/python_env.sh` contains system-level dependencies for Python installation via pyenv, including build tools and SSL libraries.

## Project Architecture

The codebase follows a modular structure with clear separation of concerns:

### Core Modules

1. **integrations/** - Bank integration layer
   - Module docstring: "Модуль для интеграции с банками" (Bank integration module)
   - Contains Python code for connecting and interacting with banking systems

2. **trading_strategies/** - Trading strategy engine
   - Module docstring: "Модуль для торговых стратегий и их обучения" (Trading strategies and training module)
   - Houses trading algorithms and machine learning training logic

3. **deploy/** - Deployment infrastructure (planned but not yet implemented)
   - Intended for deployment scripts and configuration

4. **orchestration/** - Process orchestration (planned but not yet implemented)
   - Intended for coordinating trading processes and workflows

5. **scripts/** - Development and maintenance utilities
   - Contains environment setup scripts

### Module Integration

The architecture suggests a pipeline flow:
- **integrations** provides data from banks
- **trading_strategies** processes data and generates trading signals
- **orchestration** coordinates the execution flow
- **deploy** handles deployment to production environments

## Code Conventions

- **Language**: Code contains Russian language docstrings and comments
- **Package Mode**: pyproject.toml specifies `package-mode = false`, indicating this is an application rather than a library
- **Module Versioning**: Each module has `__version__ = "0.1.0"` in its `__init__.py`

## Notes

This is an early-stage project. Many planned modules (deploy/, orchestration/) exist in the README but not yet in the filesystem. When adding functionality, follow the established module structure and maintain version consistency across modules.
