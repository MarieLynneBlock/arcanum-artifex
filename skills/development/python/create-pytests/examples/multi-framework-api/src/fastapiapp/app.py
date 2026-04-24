from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException

from fastapiapp.models import ItemCreate, ItemRecord, _counter, _store


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def create_app() -> FastAPI:
    application = FastAPI(lifespan=lifespan)

    @application.get("/items")
    def list_items() -> list[ItemRecord]:
        return list(_store.values())

    @application.get("/items/{item_id}")
    def get_item(item_id: int) -> ItemRecord:
        item = _store.get(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="not found")
        return item

    @application.post("/items", status_code=201)
    def create_item(body: ItemCreate) -> ItemRecord:
        _counter[0] += 1
        item = ItemRecord(id=_counter[0], name=body.name, price=body.price)
        item.save()
        return item

    @application.delete("/items/{item_id}", status_code=204)
    def delete_item(item_id: int) -> None:
        item = _store.pop(item_id, None)
        if item is None:
            raise HTTPException(status_code=404, detail="not found")

    return application


app = create_app()
