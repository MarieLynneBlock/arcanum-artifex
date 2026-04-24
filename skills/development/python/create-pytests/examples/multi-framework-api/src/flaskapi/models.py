from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_items: dict[int, Item] = {}
_counter: list[int] = [0]


@dataclass
class Item:
    id: int
    name: str
    price: float

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "price": self.price}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Item:
        name = data.get("name")
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("'name' is required and must be a non-empty string")
        price = data.get("price")
        if price is None or not isinstance(price, (int, float)) or isinstance(price, bool) or price <= 0:
            raise ValueError("'price' must be a positive number")
        _counter[0] += 1
        return cls(id=_counter[0], name=name, price=float(price))

    def save(self) -> None:
        _items[self.id] = self
