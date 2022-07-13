import copy
import json
import os

from typing import Optional
from utils import log
from utils.log import console
from vscode.extension import VSCodeExtension

_DB_PATH = "db.json"
_instance = None

def _get_instance() -> dict:
    global _instance
    if _instance is None:
        if not os.path.isfile(_DB_PATH):
            _create_database()
        with open(_DB_PATH, "r") as db:
            _instance = json.loads(db.read())
    return _instance

def _create_database() -> None:
    with open(_DB_PATH, "w") as db:
        db.write("""{
            "extensions": {}
        }""")

def commit() -> None:
    with open(_DB_PATH, "w") as db:
        db.write(json.dumps(_get_instance()))

def get_extension(id) -> dict:
    extensions = _get_instance()["extensions"]
    if id in extensions:
        return copy.deepcopy(extensions[id])
    return None

def create_extension(
    id: str,
    name: str,
    publisher: str,
    last_updated: str,
    version: Optional[str] = None,
    sha256: Optional[str] = None
) -> None:
    extensions = _get_instance()["extensions"]
    extensions[id] = {
        "id": id,
        "name": name,
        "publisher": publisher,
        "last_updated": last_updated,
        "version": version,
        "sha256": sha256
    }

def modify_extensions(new_extensions: list[dict]) -> None:
    for e in new_extensions:
        create_extension(**e)
    commit()

def update_extensions(new_extensions: list[dict]):
    new_extensions_count = 0
    updated_extensions_count = 0
    with console.status("[bold yellow]Updating database..."):
        for new_e in new_extensions:
            old_e = get_extension(new_e["id"])
            if old_e is None or old_e["last_updated"] != new_e["last_updated"]:
                create_extension(**new_e)
                if old_e is None:
                    new_extensions_count += 1
                else:
                    updated_extensions_count += 1
    commit()
    log.success("Updated database")
    log.info(f"There are {new_extensions_count} new extensions")
    log.info(f"There are {updated_extensions_count} updated extensions")

def get_all_extensions() -> list[dict]:
    return copy.deepcopy(_get_instance()["extensions"])