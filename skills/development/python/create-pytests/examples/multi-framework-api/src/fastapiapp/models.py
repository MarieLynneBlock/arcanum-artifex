from __future__ import annotations

from pydantic import BaseModel, field_validator

_store: dict[int, ItemRecord] = {}
_counter: list[int] = [0]


class ItemCreate(BaseModel):
    name: str
    price: float

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("'name' must be a non-empty string")
        return v

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("'price' must be a positive number")
        return v


class ItemRecord(BaseModel):
    id: int
    name: str
    price: float

    def save(self) -> None:
        _store[self.id] = self
