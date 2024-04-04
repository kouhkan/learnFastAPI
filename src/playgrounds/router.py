from enum import Enum
from typing import Dict, List, Union

from fastapi import APIRouter, Body, Cookie, Header, Path, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, HttpUrl
from typing_extensions import Annotated

router = APIRouter()

items = {
    "private": {
        1: "item 1",
        2: "item 2",
        3: "item 3",
    },
    "public": {
        4: "item 4",
        5: "item 5",
    },
}


@router.get("/items/{id}")
async def get_item(id: int):
    if id not in items.keys():
        return {"message": "Item not found"}
    return {id: items.get(id)}


@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


class ItemType(str, Enum):
    private = "private"
    public = "public"


@router.get("/items/type/{type}")
async def item_type(type: ItemType):
    return items[type.value]


fake_db = [{id: f"item number {id}"} for id in range(100)]


@router.get("/items/")
def read_items(skip: int = 0, limit: int = 5):
    return fake_db[skip: limit + skip]


db = []


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@router.post("/items/")
async def create_item(item: Item):
    return item


@router.post("/i/{item_id}")
async def get_i_item(
    item_id: int,
    item: Item,
    q: Annotated[Union[str, None], Query(max_length=10)] = None,
):
    items = item.model_dump()
    if q:
        items.update({"q": q})
    items.update({"id": item_id})
    return items


@router.get("/")
async def t(q: Annotated[Union[List[str], None], Query()] = None):
    if q:
        return q

    return {}


@router.post("/u/{user_id}")
async def user(user_id: Annotated[int, Path(title="User id in path")], role: Annotated[str, Query(min_length=4, max_length=5)] = "admin"):
    return {}


class Image(BaseModel):
    url: HttpUrl
    title: Union[str, None] = None


class UserBase(BaseModel):
    username: str = Field(
        max_length=64, description="Unique identifier for each user")
    email: str
    images: Union[List[Image], None] = None


class UserInput(UserBase):
    password: str
    re_password: str


class UserOutput(UserBase):
    pass


@router.post("/user/create")
async def create_user(user: UserInput, item: Annotated[Item, Body(embed=True)]):
    d = {}
    d["data"] = user.dict()
    d["data"].update(item.dict())
    # return {"data": {"user": user, "item": item}}
    return d


@router.post("/idx")
async def index_calculator(weight: Dict[int, str]):
    return weight


@router.get("/ads")
async def ads(
    ads_id: Annotated[Union[str, None], Cookie()] = None,
    user_agent: Annotated[Union[str, None], Header()] = None
):
    return {"id": ads_id, "user_agent": user_agent}


@router.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
