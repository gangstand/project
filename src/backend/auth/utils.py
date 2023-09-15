import bcrypt
from sqlalchemy import select, update
from sqlalchemy.orm import load_only
from auth import models
from auth.models import UserRoleAssociation


def get_hashed_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


async def add_user(db, **kwargs):
    user = models.User(hashed_password=kwargs['password'], email=kwargs['email'])
    db.add(user)
    await db.commit()


async def auth(db, **kwargs):
    stmt = select(models.User).where(models.User.email == kwargs['email'])
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user


async def get_user(db, **kwargs):
    stmt = select(models.User).where(models.User.email == kwargs['email'])
    stmt = stmt.options(load_only(
        models.User.last_name, models.User.first_name, models.User.email, models.User.is_superuser,
        models.User.is_verified, models.User.middle_name, models.User.avatar
    ))
    result = await db.execute(stmt)
    user = result.scalars().first()

    return user


async def get_role(db, **kwargs):
    stmt = select(models.Role).join(UserRoleAssociation).join(models.User).where(models.User.email == kwargs['email'])
    result = await db.execute(stmt)
    rows = result.fetchall()
    return [row[0] for row in rows]


async def path_user(db, **kwargs):
    stmt = update(models.User).where(models.User.email == kwargs['email']).values(
        last_name=kwargs['last_name'], first_name=kwargs['first_name'], middle_name=kwargs['middle_name']
    )
    await db.execute(stmt)
    await db.commit()


async def path_user_avatar(db, **kwargs):
    stmt = update(models.User).where(models.User.email == kwargs['email']).values(
        avatar=kwargs['avatar']
    )
    await db.execute(stmt)
    await db.commit()
