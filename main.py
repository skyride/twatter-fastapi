import json, os
from uuid import UUID, uuid4
from typing import Dict

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from redis import Redis
from pydantic import BaseModel


app = FastAPI()
redis = Redis(os.environ.get("REDIS_URL", "127.0.0.1"))
EXPIRES = 3600


class Item(BaseModel):
    id: UUID = None
    name: str


@app.get("/items/")
def list_items():
    """
    List all items.
    """
    return [
        json.loads(redis.get(key))
        for key in redis.keys("items:*")]


@app.get("/items/{pk}")
def get_item(pk: UUID):
    """
    Get a single item.
    """
    item = redis.get(f"items:{pk}")
    if item is None:
        return JSONResponse(
            content={"message": "Not Found"},
            status_code=status.HTTP_404_NOT_FOUND)

    return json.loads(item)


@app.post("/items/")
def create_item(item: Item):
    """
    Create a single item.
    """
    item.id = uuid4()
    redis.set(
        f"items:{item.id}", json.dumps(item.dict(), default=str),
        ex=EXPIRES)
    return item


@app.put("/items/{pk}")
def update_item(pk: UUID, item: Item):
    """
    Update a single item.
    """
    if not redis.exists(f"items:{pk}"):
        return JSONResponse(
        content={"message": "Not Found"},
        status_code=status.HTTP_404_NOT_FOUND)

    item.id = pk
    redis.set(
        f"items:{item.id}", json.dumps(item.dict(), default=str),
        ex=EXPIRES)

    return item
