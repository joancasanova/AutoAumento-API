from fastapi import APIRouter, HTTPException
from app.interfaces.api.schemas.requests import SetupDataRequest
from app.infrastructure.adapters.setups_service import get_setups_repo
from app.application.use_cases.manage_setups_use_case import ManageSetupsUseCase
from app.domain.entities import SetupData

router = APIRouter()

@router.get("/")
def get_all_setups():
    repo = get_setups_repo()
    use_case = ManageSetupsUseCase(repo)
    return {"setups": use_case.list_setups()}

@router.get("/{name}")
def get_setup(name: str):
    repo = get_setups_repo()
    use_case = ManageSetupsUseCase(repo)
    data = use_case.load_setup(name)
    if data is None:
        raise HTTPException(status_code=404, detail="Setup not found")
    return data

@router.post("/{name}")
def post_setup(name: str, setup_data: SetupDataRequest):
    repo = get_setups_repo()
    use_case = ManageSetupsUseCase(repo)
    sd = SetupData(setup_data.model, setup_data.generation_prompts, setup_data.verification_prompts, setup_data.reference_data)
    use_case.save_setup(name, sd)
    return {"status":"saved"}

@router.delete("/{name}")
def remove_setup(name:str):
    repo = get_setups_repo()
    use_case = ManageSetupsUseCase(repo)
    success = use_case.delete_setup(name)
    if not success:
        raise HTTPException(status_code=404, detail="Setup not found")
    return {"status":"deleted"}
