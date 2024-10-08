import json
from pathlib import Path


async def load_product_data() -> dict:
    file_path = Path("products.json")
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}
