from typing import Dict
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Column, MetaData, String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from database import Base
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

storage = FileSystemStorage(path="./media/user")


def __setattr__(self, name, value):
    """ No objects are immutable """
    pass


uuid.UUID.__setattr__ = __setattr__


class UserRoleAssociation(Base):
    __tablename__ = "user_role"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"), primary_key=True)


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    last_name: Mapped[str] = mapped_column(String(length=320), nullable=True)
    first_name: Mapped[str] = mapped_column(String(length=320), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(length=320), nullable=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    avatar = Column(FileType(storage=storage))
    roles = relationship("Role", secondary=UserRoleAssociation.__table__, back_populates="users")


class Role(Base):
    __tablename__ = "role"

    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(length=320), nullable=True)
    permission: Mapped[Dict] = mapped_column(JSON, nullable=True)
    users = relationship("User", secondary=UserRoleAssociation.__table__, back_populates="roles")