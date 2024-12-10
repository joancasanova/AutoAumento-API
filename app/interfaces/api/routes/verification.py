# interfaces/api/routes/verification.py
from fastapi import APIRouter, HTTPException
from typing import Any
from app.interfaces.api.schemas.requests import VerificationRequest
from app.infrastructure.adapters.llm_service import get_llm
from app.infrastructure.adapters.embeddings_service import get_embedder
from app.domain.services.verifier_service import VerifierService
from app.application.use_cases.verify_text_use_case import VerifyTextUseCase
from app.domain.entities import (ParsedResult, ParseEntry,
                                VerificationMethod, VerificationMethodType, VerificationMethodMode,
                                VerificationProcess, EmbeddingVerificationSettings, ConsensusVerificationSettings)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", summary="Verificar resultado parseado", description="Dado un resultado parseado (GeneratedResultToVerify) y un VerificationProcess, aplica métodos de verificación (embedding, consensus) y determina el estado final.")
def verify_result(req: VerificationRequest) -> Any:
    logger.info(f"Received verification request: {req}")
    """
    Este endpoint recibe:
    - entries: Lista de entradas (placeholder:valor) resultantes del parseo. Esto forma el GeneratedResultToVerify.
    - process: Configuración del proceso de verificación (VerificationProcessRequest), que contiene una lista de métodos (VerificationMethodRequest).

    Cada VerificationMethodRequest:
    - `name`: Nombre del método
    - `type`: 'embedding' o 'consensus'
    - `mode`: 'eliminatorio' o 'acumulativo'
    - `embedding_settings` (si tipo embedding): lower_threshold, upper_threshold, reference_text
    - `consensus_settings` (si tipo consensus): system_prompt, user_prompt, placeholders, positive_responses, num_responses, num_positive_required, max_new_tokens

    El resultado final:
    - `verification_methods_passed`: Métodos superados
    - `verification_methods_failed`: Métodos fallados
    - `final_status`: 'confirmada', 'a revisar' o 'descartada'
    - `entries`: Las mismas entradas con su data.
    """
    entries = [ParseEntry(ed) for ed in req.entries]
    to_verify = ParsedResult(entries)

    methods = []
    for m in req.process.methods:
        method_type = VerificationMethodType(m.type.lower())
        mode = VerificationMethodMode(m.mode.lower())
        embedding_settings = None
        consensus_settings = None

        if method_type == VerificationMethodType.EMBEDDING and m.embedding_settings:
            embedding_settings = EmbeddingVerificationSettings(
                lower_threshold=m.embedding_settings["lower_threshold"],
                upper_threshold=m.embedding_settings["upper_threshold"],
                reference_text=m.embedding_settings["reference_text"]
            )
        if method_type == VerificationMethodType.CONSENSUS and m.consensus_settings:
            consensus_settings = ConsensusVerificationSettings(
                system_prompt=m.consensus_settings["system_prompt"],
                user_prompt=m.consensus_settings["user_prompt"],
                placeholders=m.consensus_settings["placeholders"],
                positive_responses=m.consensus_settings["positive_responses"],
                num_responses=m.consensus_settings["num_responses"],
                num_positive_required=m.consensus_settings["num_positive_required"],
                max_new_tokens=m.consensus_settings["max_new_tokens"]
            )

        method = VerificationMethod(
            name=m.name,
            method_type=method_type,
            mode=mode,
            embedding_settings=embedding_settings,
            consensus_settings=consensus_settings
        )
        methods.append(method)

    process = VerificationProcess(
        methods=methods,
        required_for_confirmed=req.process.required_for_confirmed,
        required_for_review=req.process.required_for_review
    )

    llm = get_llm()
    embedder = get_embedder()
    verifier_service = VerifierService()
    use_case = VerifyTextUseCase(verifier_service, embedder.get_similarity, llm.generate)

    verified_result = use_case.execute(to_verify, process)

    logger.info(f"Verification result: {verified_result}")
    return {
        "verification_methods_passed": verified_result.verification_methods_passed,
        "verification_methods_failed": verified_result.verification_methods_failed,
        "final_status": verified_result.final_status,
        "entries": [e.data for e in verified_result.entries]
    }