import pytz
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from ..module.models import Base


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    file_path = Column(String(128), unique=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/Moscow")).replace(
            tzinfo=None
        ),
    )
    last_updated_at = Column(DateTime, default=None)
