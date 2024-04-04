from fastapi import FastAPI

from database import Base, engine
from users.router import router as users_router
from playgrounds.router import router as p_routers

app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(p_routers, prefix="/p", tags=["playgrounds"])
