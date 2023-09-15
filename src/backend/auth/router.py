import os
import uuid
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, APIRouter, UploadFile
from auth_settings import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from auth.schemas import UserLogin, User, UserUpdate
from auth.utils import (
    get_hashed_password, verify_password, add_user, auth, get_user, path_user, path_user_avatar,
    get_role
)
from database import get_db

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["Auth"], responses={404: {"description": "Not found"}})


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('SECRET')


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def post_signup(user: User, db: Session = Depends(get_db)):
    password = get_hashed_password(password=user.password).decode()
    await add_user(db, email=user.email, password=password)
    return {"message": "success"}


@router.post("/login", status_code=status.HTTP_200_OK, summary="login user")
async def post_login(user: UserLogin, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user_db = await auth(db, email=user.email)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    if verify_password(password=user.password, hashed_password=user_db.hashed_password.encode()):
        access_token = authorize.create_access_token(subject=user.email)
        return {"access": access_token}


@router.get("/verify", status_code=status.HTTP_200_OK, )
async def get_verify(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e
    current_user = authorize.get_jwt_subject()
    return {"email": current_user}


@router.get("/me", status_code=status.HTTP_200_OK, )
async def get_me(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e
    current_user = authorize.get_jwt_subject()
    user = await get_user(db, email=current_user)
    return user


@router.patch("/me", status_code=status.HTTP_200_OK)
async def path_me(
        user: UserUpdate,
        authorize: AuthJWT = Depends(),
        db: Session = Depends(get_db)
):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e
    current_user = authorize.get_jwt_subject()

    await path_user(
        db, email=current_user, last_name=user.last_name,
        first_name=user.first_name, middle_name=user.middle_name
    )
    return await get_user(db, email=current_user)


@router.patch("/me/avatar", status_code=status.HTTP_200_OK)
async def path_me_avatar(
        avatar: UploadFile,
        authorize: AuthJWT = Depends(),
        db: Session = Depends(get_db)
):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e
    current_user = authorize.get_jwt_subject()

    name = avatar.filename

    avatar.filename = f"{uuid.uuid4()}.{name.split('.')[-1]}"

    await path_user_avatar(
        db, email=current_user, avatar=avatar
    )
    return await get_user(db, email=current_user)


@router.get("/me/role", status_code=status.HTTP_200_OK)
async def get_me_role(
        authorize: AuthJWT = Depends(),
        db: Session = Depends(get_db)
):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e
    current_user = authorize.get_jwt_subject()

    return await get_role(db, email=current_user)
