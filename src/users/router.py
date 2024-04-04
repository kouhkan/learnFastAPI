from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from users.schemas import UserRegisterInput, UpdateUserInput, UserLoginInput, JWTPayload
from users.service import UserService
from users.utils import JWTHandler

router = APIRouter()


@router.post("/")
async def create_user(db_session: Annotated[AsyncSession, Depends(get_db)], data: UserRegisterInput = Body()):
    user = await UserService(db_session).create(
        username=data.username,
        email=data.email,
        password=data.password
    )
    return user


@router.get("/{username}")
async def get_user_by_username(db_session: Annotated[AsyncSession, Depends(get_db)], username: str):
    user = await UserService(db_session).get_user_by_username(username)
    return user


@router.patch("/username")
async def update_username(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        data: UpdateUserInput = Body(),
        token: JWTPayload = Depends(JWTHandler.verify_token)
):
    user = await UserService(db_session).update_username(old_username=token.username, new_username=data.new_username)
    return user


@router.delete("/", status_code=204)
async def delete_user(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        token: JWTPayload = Depends(JWTHandler.verify_token)
):
    await UserService(db_session).delete_user(username=token.username)
    return {}


@router.post("/login")
async def login(db_session: Annotated[AsyncSession, Depends(get_db)], data: UserLoginInput = Body()):
    user = await UserService(db_session).login(**data.__dict__)
    return user
