import random
from sqlalchemy import MetaData, String
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from database import Base
from fastapi_users_db_sqlalchemy.generics import GUID

metadata = MetaData()


def generate_unique_tag():
    return ''.join(random.sample('0123456789', 10))


class Customers(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(length=320), nullable=True)
    iin: Mapped[str] = mapped_column(String(length=320), nullable=True)
    tag: Mapped[int] = mapped_column(String(length=10), nullable=False, default=generate_unique_tag, unique=True)
