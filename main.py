from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
from datetime import date, datetime
from typing import Optional

from database import get_db, init_db
from models import Activity, BabyProfile
from routers import activities, profiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: cleanup if needed


# Helper functions
def calculate_age_in_weeks(birthday: date) -> int:
    """Calculate baby's age in weeks from birthday."""
    today = date.today()
    age_days = (today - birthday).days
    age_weeks = age_days // 7
    return age_weeks


async def get_profile_context(db: AsyncSession) -> dict:
    """Get profile context for templates including baby info and current role."""
    # Get current profile
    profile_result = await db.execute(select(BabyProfile))
    current_profile = profile_result.scalar_one_or_none()

    if not current_profile:
        return {
            "profile": None,
            "baby_age_weeks": None,
            "current_date": date.today(),
            "current_role": None
        }

    # Calculate age in weeks
    age_weeks = calculate_age_in_weeks(current_profile.birthday)

    # Get most recent activity to determine current role
    recent_activity_result = await db.execute(
        select(Activity).order_by(Activity.created_at.desc()).limit(1)
    )
    recent_activity = recent_activity_result.scalar_one_or_none()
    current_role = recent_activity.role if recent_activity and recent_activity.role else "Not set"

    return {
        "profile": current_profile,
        "baby_age_weeks": age_weeks,
        "current_date": date.today(),
        "current_role": current_role
    }


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
app.include_router(profiles.router)


# Template routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    """Display the dashboard with all activities."""
    # Get profile context for navbar
    profile_context = await get_profile_context(db)

    # Get activities
    result = await db.execute(
        select(Activity).order_by(Activity.start_time.desc()).limit(50)
    )
    activities_list = result.scalars().all()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "activities": activities_list, **profile_context}
    )


@app.get("/add", response_class=HTMLResponse)
async def add_activity_form(request: Request, db: AsyncSession = Depends(get_db)):
    """Display form to add a new activity."""
    # Get profile context for navbar
    profile_context = await get_profile_context(db)

    return templates.TemplateResponse(
        "activity_form.html",
        {"request": request, "activity": None, **profile_context}
    )


@app.get("/edit/{activity_id}", response_class=HTMLResponse)
async def edit_activity_form(
    request: Request,
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Display form to edit an existing activity."""
    # Get profile context for navbar
    profile_context = await get_profile_context(db)

    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()

    return templates.TemplateResponse(
        "activity_form.html",
        {"request": request, "activity": activity, **profile_context}
    )


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, db: AsyncSession = Depends(get_db)):
    """Display the settings page."""
    # Get profile context for navbar
    profile_context = await get_profile_context(db)

    return templates.TemplateResponse(
        "settings.html",
        {"request": request, **profile_context}
    )


@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request, db: AsyncSession = Depends(get_db)):
    """Display the analytics page with activity insights."""
    # Get profile context for navbar
    profile_context = await get_profile_context(db)

    # Get all activities ordered by start time
    result = await db.execute(
        select(Activity).order_by(Activity.start_time.desc())
    )
    activities_list = result.scalars().all()

    return templates.TemplateResponse(
        "analytics.html",
        {"request": request, "activities": activities_list, **profile_context}
    )


@app.get("/timeline", response_class=HTMLResponse)
async def timeline_page(request: Request, db: AsyncSession = Depends(get_db)):
    """Display the timeline page with chronological activity view."""
    # Get profile context for navbar
    profile_context = await get_profile_context(db)

    # Get all activities ordered by start time (newest first)
    result = await db.execute(
        select(Activity).order_by(Activity.start_time.desc())
    )
    activities_list = result.scalars().all()

    return templates.TemplateResponse(
        "timeline.html",
        {"request": request, "activities": activities_list, **profile_context}
    )


# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "Baby Activity Tracker is running"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=7999)