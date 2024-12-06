from fastapi import APIRouter
from app.interfaces.api.schemas.requests import GenerationRequest
from app.infrastructure.adapters.llm_service import get_llm
from app.application.use_cases.generate_text_use_case import GenerateTextUseCase
from typing import Any

router = APIRouter()

@router.post("/")
def generate_text(req: GenerationRequest) -> Any:
    llm = get_llm(req.model)
    use_case = GenerateTextUseCase(llm)
    results = use_case.execute(
        system_prompt=req.system_prompt,
        user_prompt=req.user_prompt,
        num_return_sequences=req.num_return_sequences,
        max_new_tokens=req.max_new_tokens,
        num_executions=req.num_executions,
        reference_data=req.reference_data
    )
    # Convertir a JSON
    return {"results": [ {"input":r.input, "output":r.output, "verification_status":r.verification_status} for r in results ]}
