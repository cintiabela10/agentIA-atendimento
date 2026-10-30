import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "data_base.json"

def load_db() -> dict:
    with open(DB_PATH, "r",  encoding="utf-8") as f:
        return json.load(f)

def save_db(data: dict) -> None:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)