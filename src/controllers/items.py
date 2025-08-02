from src.models.items import Items
from src.repositories.get_all import get_all


def handle_get_items():
    items = get_all(Items)

    return items
