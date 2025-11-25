import json
from pathlib import Path


DB_FILE = Path("app/data/produtos.json")

def ler_db():
    if not DB_FILE.exists():
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
