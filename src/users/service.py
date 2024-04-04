import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import WrongPasswordException, UserNotFoundException, DuplicateUserException
from users.models import User
from users.schemas import UserRegisterOutput, JWTResponsePayload
from users.utils import password_context, JWTHandler


class UserService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username: str, email: str, password: str) -> UserRegisterOutput:
        user = User(username=username, email=email, password=password_context.hash(password))

        async with self.db_session as session:
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                raise DuplicateUserException()

        return UserRegisterOutput(**user.__dict__)

    async def get_user_by_username(self, username: str) -> User:
        query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user = await session.scalar(query)

            if not user:
                raise UserNotFoundException()

        return user

    async def update_username(self, old_username: str, new_username: str) -> User:
        get_user_query = sa.select(User).where(User.username == old_username)
        update_username_query = sa.update(User).where(User.username == old_username).values(username=new_username)

        async with self.db_session as session:
            user = await session.scalar(get_user_query)

            if not user:
                raise UserNotFoundException()

            await session.execute(update_username_query)
            await session.commit()

        user.username = new_username
        return user

    async def delete_user(self, username: str) -> None:
        query = sa.delete(User).where(User.username == username)

        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

        return None

    async def login(self, username: str, password: str) -> JWTResponsePayload:
        query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user = await session.scalar(query)

            if not user:
                raise UserNotFoundException()

        if not password_context.verify(password, user.password):
            raise WrongPasswordException()

        return JWTHandler.generate(username)
