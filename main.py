from uuid import UUID, uuid4
from typing import Optional, Dict

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    id: UUID = None
    name: str


items: Dict[UUID, Item] = {}


@app.get("/items/")
def list_items():
    """
    List all items.
    """
    return list(items.values())


@app.get("/items/{pk}")
def get_item(pk: UUID):
    """
    Get a single item.
    """
    if pk not in items:
        return JSONResponse(
        content={"message": "Not Found"},
        status_code=status.HTTP_404_NOT_FOUND)

    return items[pk]


@app.post("/items/")
def create_item(item: Item):
    """
    Create a single item.
    """
    item.id = uuid4()
    items[item.id] = item
    return item


@app.put("/items/{pk}")
def update_item(pk: UUID, item: Item):
    """
    Update a single item.
    """
    if pk not in items:
        return JSONResponse(
        content={"message": "Not Found"},
        status_code=status.HTTP_404_NOT_FOUND)

    item.id = pk
    items[pk] = item

    return item
