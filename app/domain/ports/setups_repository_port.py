from typing import Optional, Dict, Any, List

class SetupsRepositoryPort:
    def load_setup(self, name: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    def save_setup(self, name: str, data: Dict[str,Any]) -> None:
        raise NotImplementedError

    def list_setups(self) -> List[str]:
        raise NotImplementedError

    def delete_setup(self, name: str) -> bool:
        raise NotImplementedError
