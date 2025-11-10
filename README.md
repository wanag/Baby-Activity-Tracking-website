# Baby Activity Tracker

A web application to track your baby's daily activities including sleep, feeding, and diaper changes.

## Features

### Implemented
1. **Activity Management**: Create, view, edit, and delete baby activities (sleep, feeding, diaper changes)
2. **Dashboard**: View all activities in chronological order with filtering by activity type
3. **Quick Add**: Quickly log activities with one-click buttons
4. **SQLite Database**: All data is stored locally and persists between sessions
5. **Responsive Web Interface**: Clean, user-friendly interface that works on desktop and mobile

### Planned
- Sleep pattern prediction using collected data
- Analytics and visualizations
- Data export functionality

## Tech Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Jinja2 templates with vanilla JavaScript
- **Server**: Uvicorn ASGI server

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Open your browser to `http://localhost:7999`

## API Documentation

Interactive API documentation is available at `http://localhost:7999/docs` when the application is running.