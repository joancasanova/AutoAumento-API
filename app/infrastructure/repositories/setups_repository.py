import os
import json
from typing import Optional, Dict, Any, List
from app.domain.ports.setups_repository_port import SetupsRepositoryPort

class SetupsRepository(SetupsRepositoryPort):
    def __init__(self, directory="setups"):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def load_setup(self, name: str) -> Optional[Dict[str,Any]]:
        path = os.path.join(self.directory, f"{name}.json")
        if os.path.exists(path):
            with open(path,"r",encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_setup(self, name: str, data: Dict[str,Any]) -> None:
        path = os.path.join(self.directory, f"{name}.json")
        with open(path,"w",encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def list_setups(self) -> List[str]:
        files = os.listdir(self.directory)
        return [f.replace(".json","") for f in files if f.endswith(".json")]

    def delete_setup(self, name: str) -> bool:
        path = os.path.join(self.directory, f"{name}.json")
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
