import json, os
from uuid import UUID, uuid4
from typing import Dict

import aioredis
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    id: UUID = None
    name: str


@app.on_event("startup")
async def startup():
    app.state.redis = await aioredis.create_redis_pool(
        os.environ.get("REDIS_URL", "redis://127.0.0.1:6379"))


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()


@app.get("/items/")
async def list_items():
    """
    List all items.
    """
    return [
        json.loads(await app.state.redis.get(key))
        for key in await app.state.redis.keys("items:*")]


@app.get("/items/{pk}")
async def get_item(pk: UUID):
    """
    Get a single item.
    """
    item = await app.state.redis.get(f"items:{pk}")
    if item is None:
        return JSONResponse(
            content={"message": "Not Found"},
            status_code=status.HTTP_404_NOT_FOUND)

    return json.loads(item)


@app.post("/items/")
async def create_item(item: Item):
    """
    Create a single item.
    """
    item.id = uuid4()
    await app.state.redis.set(
        f"items:{item.id}", json.dumps(item.dict(), default=str))
    return item


@app.put("/items/{pk}")
async def update_item(pk: UUID, item: Item):
    """
    Update a single item.
    """
    if not await app.state.redis.exists(f"items:{pk}"):
        return JSONResponse(
        content={"message": "Not Found"},
        status_code=status.HTTP_404_NOT_FOUND)

    item.id = pk
    await app.state.redis.set(
        f"items:{item.id}", json.dumps(item.dict(), default=str))

    return item
