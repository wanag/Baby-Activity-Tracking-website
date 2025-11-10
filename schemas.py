from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from models import ActivityType


class ActivityBase(BaseModel):
    activity_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    notes: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    activity_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    notes: Optional[str] = None


class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
