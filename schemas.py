from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional
from models import ActivityType


class ActivityBase(BaseModel):
    activity_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    notes: Optional[str] = None

    @field_validator('start_time', 'end_time')
    @classmethod
    def ensure_timezone_aware(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Ensure datetime is timezone-aware and convert to UTC."""
        if v is None:
            return v
        if v.tzinfo is None:
            # If naive, assume UTC
            return v.replace(tzinfo=timezone.utc)
        # Convert to UTC
        return v.astimezone(timezone.utc)


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    activity_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    notes: Optional[str] = None

    @field_validator('start_time', 'end_time')
    @classmethod
    def ensure_timezone_aware(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Ensure datetime is timezone-aware and convert to UTC."""
        if v is None:
            return v
        if v.tzinfo is None:
            # If naive, assume UTC
            return v.replace(tzinfo=timezone.utc)
        # Convert to UTC
        return v.astimezone(timezone.utc)


class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime

    model_config = {
        'from_attributes': True,
        'json_encoders': {
            datetime: lambda v: v.isoformat() if v else None
        }
    }
