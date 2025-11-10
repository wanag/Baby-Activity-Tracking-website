from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Activity
from schemas import ActivityCreate, ActivityUpdate, ActivityResponse

router = APIRouter(prefix="/api/activities", tags=["activities"])


@router.post("/", response_model=ActivityResponse, status_code=201)
async def create_activity(
    activity: ActivityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new activity."""
    db_activity = Activity(**activity.model_dump())
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    return db_activity


@router.get("/", response_model=List[ActivityResponse])
async def list_activities(
    activity_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all activities with optional filters."""
    query = select(Activity)

    if activity_type:
        query = query.where(Activity.activity_type == activity_type)

    if start_date:
        query = query.where(Activity.start_time >= start_date)

    if end_date:
        query = query.where(Activity.start_time <= end_date)

    query = query.order_by(Activity.start_time.desc()).limit(limit)

    result = await db.execute(query)
    activities = result.scalars().all()
    return activities


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific activity by ID."""
    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    return activity


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing activity."""
    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Update only provided fields
    update_data = activity_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(activity, key, value)

    await db.commit()
    await db.refresh(activity)
    return activity


@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete an activity."""
    result = await db.execute(
        select(Activity).where(Activity.id == activity_id)
    )
    activity = result.scalar_one_or_none()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    await db.delete(activity)
    await db.commit()
    return None
