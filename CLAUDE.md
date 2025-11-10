# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple FastAPI web service that serves as a home server page. The application provides basic health check endpoints and runs on port 7999.

## Architecture

- **main.py**: Single-file FastAPI application with two endpoints:
  - `/`: Root endpoint returning server status
  - `/test`: Test endpoint for verification

The application uses Uvicorn as the ASGI server and is configured to run on all interfaces (0.0.0.0) on port 7999.

## Development Commands

### Environment Setup
```bash
# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run the FastAPI server directly
python main.py

# Or run with uvicorn directly with auto-reload
uvicorn main:app --host 0.0.0.0 --port 7999 --reload
```

### Testing Endpoints
```bash
# Test root endpoint
curl http://localhost:7999/

# Test the test endpoint
curl http://localhost:7999/test
```

## Key Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation (FastAPI dependency)
