# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Baby Activity Tracker is a web application for tracking daily baby activities including sleep, feeding, and diaper changes. Built with FastAPI, SQLAlchemy, and server-side rendered templates using Jinja2.

## Architecture

### Core Components

- **main.py**: Application entry point with FastAPI setup, template routes, and lifespan management
  - Template routes: `/` (dashboard), `/add` (add activity), `/edit/{id}` (edit activity)
  - Health check: `/api/health`
  - Database initialization on startup

- **database.py**: Database configuration and session management
  - Async SQLite database with SQLAlchemy
  - Database file: `baby_tracker.db` (auto-created on first run)
  - Session dependency injection via `get_db()`

- **models.py**: SQLAlchemy ORM models
  - `Activity`: Main model with fields for activity_type, start_time, end_time, notes, created_at
  - Activity types: sleep, feeding, diaper

- **schemas.py**: Pydantic models for request/response validation
  - `ActivityCreate`, `ActivityUpdate`, `ActivityResponse`

- **routers/activities.py**: REST API endpoints for CRUD operations
  - POST `/api/activities/` - Create activity
  - GET `/api/activities/` - List activities (with filters)
  - GET `/api/activities/{id}` - Get single activity
  - PUT `/api/activities/{id}` - Update activity
  - DELETE `/api/activities/{id}` - Delete activity

### Frontend Structure

- **templates/**: Jinja2 HTML templates
  - `base.html`: Base template with navigation and layout
  - `dashboard.html`: Main dashboard with activity list and quick-add buttons
  - `activity_form.html`: Form for adding/editing activities

- **static/**: Static assets
  - `css/style.css`: Application styles

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
# Run the FastAPI server with auto-reload
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 7999 --reload

# Access the application
# Web UI: http://localhost:7999/
# API docs: http://localhost:7999/docs
```

### Testing API Endpoints
```bash
# Health check
curl http://localhost:7999/api/health

# Create an activity
curl -X POST http://localhost:7999/api/activities/ \
  -H "Content-Type: application/json" \
  -d '{"activity_type": "sleep", "start_time": "2025-11-10T10:00:00"}'

# List all activities
curl http://localhost:7999/api/activities/

# Filter by activity type
curl "http://localhost:7999/api/activities/?activity_type=sleep"

# Update an activity
curl -X PUT http://localhost:7999/api/activities/1 \
  -H "Content-Type: application/json" \
  -d '{"end_time": "2025-11-10T12:00:00", "notes": "Good nap"}'

# Delete an activity
curl -X DELETE http://localhost:7999/api/activities/1
```

### Database Management

The database is automatically created on first run. To reset the database:
```bash
rm baby_tracker.db
# Restart the application to recreate the database
```

## Key Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **SQLAlchemy**: ORM for database operations
- **aiosqlite**: Async SQLite driver
- **Jinja2**: Template engine for HTML rendering
- **Pydantic**: Data validation

## Project Structure

```
.
├── main.py                 # Application entry point
├── database.py             # Database configuration
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── routers/
│   └── activities.py       # Activity API endpoints
├── templates/
│   ├── base.html           # Base template
│   ├── dashboard.html      # Dashboard view
│   └── activity_form.html  # Add/edit form
├── static/
│   └── css/
│       └── style.css       # Application styles
├── requirements.txt        # Python dependencies
└── baby_tracker.db         # SQLite database (auto-created)
```

## Future Enhancements

- Sleep pattern prediction using collected data
- User authentication for multi-user support
- Data export functionality
- Analytics and visualizations
