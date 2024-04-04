from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///blog.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = async_sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase, MappedAsDataclass):
    pass


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
