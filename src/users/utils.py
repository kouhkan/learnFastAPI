from datetime import datetime, timedelta
from typing import Union, Annotated

import jwt
from fastapi import Header, HTTPException
from jwt import PyJWTError
from passlib.context import CryptContext
from starlette import status

import config
from exceptions import ExpiredTokenException, InvalidCredentialsException, AuthenticationException
from users.schemas import JWTPayload, JWTResponsePayload

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTHandler:
    @staticmethod
    def generate(username: str, exp_timestamp: int | None = None) -> JWTResponsePayload:
        expire_time = config.BaseConfig.ACCESS_TOKEN_EXPIRE_TIME

        secret_key = config.BaseConfig.SECRET_KEY

        expires_delta = datetime.utcnow() + timedelta(days=expire_time)

        to_encode = {
            "exp": exp_timestamp if exp_timestamp else expires_delta,
            "username": username,
        }
        encoded_jwt = jwt.encode(to_encode, secret_key, config.BaseConfig.ALGORITHM)

        return JWTResponsePayload(access=encoded_jwt)

    @staticmethod
    def verify_token(auth_token: Annotated[str, Header()]) -> JWTPayload:
        jwt_token = auth_token
        if not jwt_token:
            raise AuthenticationException()
        try:
            token_data = jwt.decode(jwt_token, config.BaseConfig.SECRET_KEY, algorithms=[config.BaseConfig.ALGORITHM])

            if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
                raise ExpiredTokenException()
        except jwt.exceptions.PyJWTError:
            raise InvalidCredentialsException

        return JWTPayload(**token_data)
