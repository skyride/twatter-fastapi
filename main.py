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
    if pk in items:
        return items[pk]

    return JSONResponse(
        content={"message": "Not Found"},
        status_code=status.HTTP_404_NOT_FOUND)


@app.post("/items/")
def create_item(item: Item):
    item.id = uuid4()
    items[item.id] = item
    return item
