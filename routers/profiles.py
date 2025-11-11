from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import date
import os
import shutil
from pathlib import Path

from database import get_db
from models import BabyProfile
from schemas import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/api/profiles", tags=["profiles"])

# Define upload directory
UPLOAD_DIR = Path("static/uploads/profiles")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile(
    name: str = Form(...),
    birthday: date = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    """Create a new baby profile. Only one profile can exist at a time."""
    # Check if a profile already exists
    result = await db.execute(select(BabyProfile))
    existing_profile = result.scalar_one_or_none()

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="A baby profile already exists. Please delete the existing profile first."
        )

    # Handle photo upload
    photo_path = None
    if photo:
        # Generate unique filename
        file_extension = os.path.splitext(photo.filename)[1]
        filename = f"baby_profile{file_extension}"
        file_path = UPLOAD_DIR / filename

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        photo_path = f"/static/uploads/profiles/{filename}"

    # Create profile
    db_profile = BabyProfile(
        name=name,
        birthday=birthday,
        photo_path=photo_path
    )
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile


@router.get("/current", response_model=ProfileResponse)
async def get_current_profile(db: AsyncSession = Depends(get_db)):
    """Get the current baby profile."""
    result = await db.execute(select(BabyProfile))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="No baby profile found")

    return profile


@router.put("/{profile_id}", response_model=ProfileResponse)
async def update_profile(
    profile_id: int,
    name: Optional[str] = Form(None),
    birthday: Optional[date] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    """Update the baby profile."""
    result = await db.execute(
        select(BabyProfile).where(BabyProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Update fields
    if name is not None:
        profile.name = name
    if birthday is not None:
        profile.birthday = birthday

    # Handle photo upload
    if photo:
        # Delete old photo if exists
        if profile.photo_path:
            old_photo_path = Path(profile.photo_path.lstrip('/'))
            if old_photo_path.exists():
                old_photo_path.unlink()

        # Save new photo
        file_extension = os.path.splitext(photo.filename)[1]
        filename = f"baby_profile{file_extension}"
        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        profile.photo_path = f"/static/uploads/profiles/{filename}"

    await db.commit()
    await db.refresh(profile)
    return profile


@router.delete("/{profile_id}", status_code=204)
async def delete_profile(
    profile_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete the baby profile and all associated activities."""
    result = await db.execute(
        select(BabyProfile).where(BabyProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Delete photo if exists
    if profile.photo_path:
        photo_path = Path(profile.photo_path.lstrip('/'))
        if photo_path.exists():
            photo_path.unlink()

    # Delete profile (activities will be cascade deleted)
    await db.delete(profile)
    await db.commit()
    return None
