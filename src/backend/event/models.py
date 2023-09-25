import datetime
import uuid
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import MetaData, String, JSON, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from database import Base

metadata = MetaData()


class EventHistory(Base):
    __tablename__ = "event"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(255))
    time: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    data: Mapped[JSON] = mapped_column(JSON)
