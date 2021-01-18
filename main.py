from typing import Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


items = {}


@app.get("/items/")
def list_items():
    """
    List all items.
    """
    return list(items.values())


@app.get("/items/{pk}")
def get_item(pk: int):
    """
    Get a single item.
    """
    if pk in items:
        return items[pk]

    return JSONResponse(
        content={"message": "Not Found"},
        status_code=status.HTTP_404_NOT_FOUND)
