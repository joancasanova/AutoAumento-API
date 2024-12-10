# interfaces/api/routes/generation.py
from fastapi import APIRouter, HTTPException
from typing import Any
from app.interfaces.api.schemas.requests import GenerationRequest
from app.infrastructure.adapters.llm_service import get_llm
from app.application.use_cases.generate_text_use_case import GenerateTextUseCase
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", summary="Generar texto", description="Genera texto utilizando el modelo LLM especificado. Permite placeholders y datos de referencia para sustituir en los prompts.")
def generate_text(req: GenerationRequest) -> Any:
    logger.info(f"Received generation request: {req}")
    """
    Este endpoint recibe una configuración para generación de texto:
    - model: Nombre del modelo en HuggingFace.
    - system_prompt: Prompt de contexto (rol del asistente, etc.).
    - user_prompt: Instrucción del usuario.
    - num_return_sequences: Cuántas respuestas generar.
    - max_new_tokens: Límite de tokens a generar.
    - num_executions: Repetir la generación varias veces.
    - reference_data: Diccionario para reemplazar placeholders en los prompts.

    Retorna una lista de resultados con el `response` generado y el `verification_status` (por defecto None hasta que se verifique).
    """
    llm = get_llm(req.model)
    use_case = GenerateTextUseCase(llm)
    try:
        results = use_case.execute(
            system_prompt=req.system_prompt,
            user_prompt=req.user_prompt,
            num_return_sequences=req.num_return_sequences,
            max_new_tokens=req.max_new_tokens,
            num_executions=req.num_executions,
            reference_data=req.reference_data
        )
        logger.info(f"Generated results: {results}")
        return {"results": [{"response": r.response} for r in results]}
    except ValueError as ve:
        logger.error(f"ValueError occurred: {str(ve)}")
        raise HTTPException(400, str(ve))
    except RuntimeError as re:
        logger.error(f"RuntimeError occurred: {str(re)}")
        raise HTTPException(500, str(re))
    except Exception as e:
        logger.exception("Unexpected error occurred while generating text")
        raise HTTPException(500, "Unexpected error occurred while generating text")