# interfaces/api/routes/parse.py
from fastapi import APIRouter
from typing import Any
from app.interfaces.api.schemas.requests import ParseRequest
from app.domain.entities import GeneratedResult, ParseMultipleStrategy, ParseRule, ParseMode, ParseScope, ParseFallbackStrategy, ParseConfiguration
from app.domain.services.parse_service import ParseService
from app.application.use_cases.parse_generated_output_use_case import ParseGeneratedOutputUseCase
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", summary="Parsear texto generado", description="Aplica reglas de parseo (regex o palabras clave) al texto generado para extraer placeholders y obtener un GeneratedResultToVerify.")
def parse_result(req: ParseRequest) -> Any:
    logger.info(f"Received parse request: {req}")
    """
    Este endpoint recibe:
    - response: El texto generado por el LLM.
    - config: Configuración de parseo (ParseConfigurationRequest) que contiene una lista de ParseRuleRequest.

    Cada ParseRuleRequest indica cómo extraer un fragmento de texto (placeholder):
    - `label`: Nombre del placeholder extraído.
    - `mode`: 'regex' o 'keyword'.
    - `pattern`: Patrón principal.
    - `secondary_pattern`: Patrón de fin (opcional).
    - `scope`: 'line_by_line' o 'all_text'.
    - `fallback_strategy`: Qué hacer si no se encuentra coincidencia ('error', 'empty', 'custom').
    - `fallback_value`: Valor por defecto si fallback='custom'.

    Retorna las entradas parseadas (un array de diccionarios con placeholders y sus valores) listas para la verificación.
    """
    rules = []
    for r in req.config.rules:
        mode = ParseMode(r.mode.lower())
        scope = ParseScope(r.scope.lower())
        fallback = ParseFallbackStrategy(r.fallback_strategy.lower())
        multiple = ParseMultipleStrategy(r.multiple_strategy.lower())
        rule = ParseRule(
            label=r.label,
            mode=mode,
            pattern=r.pattern,
            secondary_pattern=r.secondary_pattern,
            scope=scope,
            fallback_strategy=fallback,
            fallback_value=r.fallback_value,
            multiple_strategy=multiple
        )
        rules.append(rule)
    config = ParseConfiguration(rules)

    result = GeneratedResult(req.response)
    use_case = ParseGeneratedOutputUseCase(ParseService())
    verify_result = use_case.execute(result, config)

    logger.info(f"Parsed result: {verify_result.entries}, Final status: {verify_result.final_status}")
    return {
        "entries": [e.data for e in verify_result.entries],
        "verification_status": verify_result.final_status
    }