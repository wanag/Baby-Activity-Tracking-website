from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager

from database import get_db, init_db
from models import Activity
from routers import activities


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="Baby Activity Tracker",
    description="Track your baby's daily activities including sleep, feeding, and diaper changes",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(activities.router)


# Template routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    """Display the dashboard with all activities."""
    result = await db.execute(
        select(Activity).order_by(Activity.start_time.desc()).limit(50)
    )
    activities_list = result.scalars().all()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "activities": activities_list}
    )


@app.get("/add", response_class=HTMLResponse)
async def add_activity_form(request: Request):
    """Display form to add a new activity."""
    return templates.TemplateResponse(
        "activity_form.html",
        {"request": request, "activity": None}
    )


@app.get("/edit/{activity_id}", response_class=HTMLResponse)
async def edit_activity_form(
    request: Request,
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Display form to edit an existing activity."""
    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()

    return templates.TemplateResponse(
        "activity_form.html",
        {"request": request, "activity": activity}
    )


# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "Baby Activity Tracker is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7999)