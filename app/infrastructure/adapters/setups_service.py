# setups_service.py
from app.infrastructure.repositories.setups_repository import SetupsRepository
from app.domain.ports.setups_repository_port import SetupsRepositoryPort

def get_setups_repo(directory="setups") -> SetupsRepositoryPort:
    return SetupsRepository(directory)