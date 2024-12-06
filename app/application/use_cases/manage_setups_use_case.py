from typing import Optional, Dict, Any, List
from app.domain.entities import SetupData
from app.domain.ports.setups_repository_port import SetupsRepositoryPort

class ManageSetupsUseCase:
    def __init__(self, repo: SetupsRepositoryPort):
        self.repo = repo

    def load_setup(self, name: str) -> Optional[Dict[str,Any]]:
        return self.repo.load_setup(name)

    def save_setup(self, name: str, data: SetupData) -> None:
        self.repo.save_setup(name, {
            "model": data.model,
            "generation_prompts": data.generation_prompts,
            "verification_prompts": data.verification_prompts,
            "reference_data": data.reference_data
        })

    def list_setups(self) -> List[str]:
        return self.repo.list_setups()

    def delete_setup(self, name: str) -> bool:
        return self.repo.delete_setup(name)
