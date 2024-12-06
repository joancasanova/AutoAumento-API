from fastapi import APIRouter
from app.interfaces.api.schemas.requests import VerificationRequest
from app.infrastructure.adapters.llm_service import get_llm
from app.infrastructure.adapters.embeddings_service import get_embedder
from app.domain.services.verifier_service import VerifierService
from app.application.use_cases.verify_text_use_case import VerifyTextUseCase
from app.domain.entities import GeneratedResult, VerificationPrompt

router = APIRouter()

@router.post("/")
def verify_results(req: VerificationRequest):
    llm = get_llm()  # Modelo por defecto, podrías permitir modificarlo
    embedder = get_embedder()
    verifier_service = VerifierService(threshold=0.9, upper_threshold=0.995, positive_responses=["Sí","sí","yes"], num_ok=4)

    prompts = []
    for p in req.verification_prompts:
        vp = VerificationPrompt(p.name, p.context, p.instruction, p.num_return_sequences, p.max_new_tokens, p.num_positive, p.positive_responses)
        prompts.append(vp)

    generated = [GeneratedResult(r["input"],r["output"]) for r in req.generated_results]

    use_case = VerifyTextUseCase(llm, embedder, verifier_service)
    verified_results = use_case.execute(prompts, generated)

    return {"results": [ {"input":r.input,"output":r.output,"verification_status":r.verification_status} for r in verified_results ]}
