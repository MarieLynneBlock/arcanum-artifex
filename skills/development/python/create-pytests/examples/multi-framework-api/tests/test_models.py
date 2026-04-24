import pytest

from flaskapi.models import Item, _counter, _items


@pytest.fixture(autouse=True)
def clear_store():
    _items.clear()
    _counter[0] = 0
    yield
    _items.clear()
    _counter[0] = 0


class TestItemFromDict:
    def test_valid_creates_item(self):
        item = Item.from_dict({"name": "Widget", "price": 9.99})
        assert item.name == "Widget"
        assert item.price == 9.99
        assert item.id == 1

    def test_increments_id_on_each_call(self):
        first = Item.from_dict({"name": "A", "price": 1.0})
        second = Item.from_dict({"name": "B", "price": 2.0})
        assert second.id == first.id + 1

    def test_missing_name_raises(self):
        with pytest.raises(ValueError, match="name"):
            Item.from_dict({"price": 9.99})

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="name"):
            Item.from_dict({"name": "   ", "price": 9.99})

    @pytest.mark.parametrize("price", [0, -1, -0.01])
    def test_non_positive_price_raises(self, price):
        with pytest.raises(ValueError, match="price"):
            Item.from_dict({"name": "Widget", "price": price})

    def test_string_price_raises(self):
        with pytest.raises(ValueError, match="price"):
            Item.from_dict({"name": "Widget", "price": "free"})


class TestItemToDict:
    def test_all_fields_present(self):
        item = Item(id=1, name="Gadget", price=4.50)
        assert item.to_dict() == {"id": 1, "name": "Gadget", "price": 4.50}


class TestItemSave:
    def test_save_persists_in_store(self):
        item = Item.from_dict({"name": "Widget", "price": 9.99})
        item.save()
        assert _items[item.id] is item

    def test_overwrite_updates_existing(self):
        item = Item(id=42, name="Old", price=1.0)
        item.save()
        updated = Item(id=42, name="New", price=2.0)
        updated.save()
        assert _items[42].name == "New"
