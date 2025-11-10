from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, TypeDecorator
from datetime import datetime, timezone
import enum
from database import Base


class TZDateTime(TypeDecorator):
    """A DateTime type that ensures timezone awareness."""
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Convert timezone-aware datetime to UTC before storing."""
        if value is not None:
            if value.tzinfo is None:
                # Assume UTC if no timezone
                value = value.replace(tzinfo=timezone.utc)
            else:
                # Convert to UTC
                value = value.astimezone(timezone.utc)
            # Store as timezone-naive UTC (SQLite doesn't support timezones)
            return value.replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        """Add UTC timezone when loading from database."""
        if value is not None:
            # SQLite stores as naive datetime, so add UTC timezone
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
        return value


class ActivityType(str, enum.Enum):
    SLEEP = "sleep"
    FEEDING = "feeding"
    DIAPER = "diaper"


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    activity_type = Column(String, nullable=False)
    start_time = Column(TZDateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    end_time = Column(TZDateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(TZDateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Activity(id={self.id}, type={self.activity_type}, start={self.start_time})>"
