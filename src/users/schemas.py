from uuid import UUID

from pydantic import BaseModel


class UserRegisterInput(BaseModel):
    username: str
    email: str
    password: str


class UserRegisterOutput(BaseModel):
    id: UUID
    username: str
    email: str


class UpdateUserInput(BaseModel):
    new_username: str


class UserLoginInput(BaseModel):
    username: str
    password: str


class JWTResponsePayload(BaseModel):
    access: str


class JWTPayload(BaseModel):
    username: str
    exp: int
