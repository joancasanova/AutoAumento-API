# interfaces/api/schemas/requests.py

from app.domain.entities import ParseFallbackStrategy, ParseMode, ParseMultipleStrategy, ParseScope
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class GenerationRequest(BaseModel):
    """
    Petición para generar texto utilizando un LLM.
    """
    model: str = Field(
        default="Qwen/Qwen2.5-Coder-3B-Instruct",
        example="Qwen/Qwen2.5-Coder-3B-Instruct",
        description="Nombre del modelo a utilizar, publicado en HuggingFace. Debe ser un modelo Instruct."
    )
    system_prompt: str = Field(
        default="A general prompt for the system",
        example="You are a programming expert assistant",
        description="Prompt de sistema (contexto) que define el rol y las instrucciones base del modelo."
    )
    user_prompt: str = Field(
        default="A concise user prompt. Can include placeholders. {placeholder1} + {placeholder2}",
        example="Write a program that determines if a program terminates.",
        description="Prompt de usuario (instrucción) que se pasará al modelo. Puede contener placeholders."
    )
    num_return_sequences: int = Field(
        default=1,
        gt=0,
        description="Número de secuencias/respuestas a retornar por la llamada al LLM."
    )
    max_new_tokens: int = Field(
        default=100,
        gt=0,
        description="Máximo número de tokens a generar en la respuesta."
    )
    num_executions: int = Field(
        default=1,
        gt=0,
        description="Número de veces a ejecutar la generación con los mismos parámetros."
    )
    reference_data: Dict[str,str] = Field(
        default={"placeholder1": "value of the placeholder1","placeholder2": "value of the placeholder2",},
        description="Diccionarios con datos para reemplazar placeholders en prompts. Debe contener las claves necesarias para todos los placeholders del prompt."
    )

class ParseRuleRequest(BaseModel):
    label: str = Field(
        default="label",
        description="Etiqueta (nombre del placeholder) que se asignará al texto extraído."
    )
    mode: ParseMode = Field(..., description="Modo de parseo: 'regex' o 'keyword'.")
    pattern: str = Field(..., description="Patrón principal. Si mode=regex, es la expresión regular. Si mode=keyword, es la palabra/símbolo inicial.")
    secondary_pattern: str = Field(
        description="Patrón secundario para el modo 'keyword' que delimita el final del texto a extraer. Si no se especifica, se toma desde pattern hasta el final."
    )
    scope: ParseScope = Field(
        description="Ámbito de aplicación: 'line_by_line' o 'all_text'. Si 'line_by_line', aplica la búsqueda línea a línea, si 'all_text', aplica sobre el texto completo."
    )
    fallback_strategy: ParseFallbackStrategy = Field(
        description="Estrategia en caso de no encontrar coincidencia: 'error' (lanza error), 'empty' (retorna cadena vacía), 'custom' (usa fallback_value)."
    )
    fallback_value: str = Field(
        description="Valor a usar si fallback_strategy='custom'."
    )
    multiple_strategy: ParseMultipleStrategy = Field(
        description="first or all"
    )

class ParseConfigurationRequest(BaseModel):
    rules: List[ParseRuleRequest] = Field(
        ...,
        description="Lista de reglas de parseo. Cada regla define cómo extraer un fragmento del texto."
    )

class ParseRequest(BaseModel):
    response: str = Field(..., description="Texto generado por el LLM que se desea parsear.")
    config: ParseConfigurationRequest = Field(..., description="Configuración completa de parseo a aplicar sobre 'response'.")

class VerificationMethodRequest(BaseModel):
    name: str = Field(..., description="Nombre del método de verificación.")
    type: str = Field(..., description="Tipo de método: 'embedding' o 'consensus'.")
    mode: str = Field(..., description="Modo: 'eliminatorio' o 'acumulativo'. 'eliminatorio' descarta el resultado si falla. 'acumulativo' suma al conteo de métodos superados.")
    embedding_settings: Dict[str,Any] = Field(
        description="Configuración para el método embedding. Debe incluir 'lower_threshold', 'upper_threshold' y 'reference_text'."
    )
    consensus_settings: Dict[str,Any] = Field(
        description="Configuración para el método consensus. Debe incluir 'system_prompt', 'user_prompt', 'placeholders', 'positive_responses', 'num_responses', 'num_positive_required' y 'max_new_tokens'."
    )

class VerificationProcessRequest(BaseModel):
    methods: List[VerificationMethodRequest] = Field(
        ...,
        description="Lista de métodos de verificación a aplicar en cadena."
    )
    required_for_confirmed: int = Field(
        ...,
        description="Cantidad de métodos acumulativos que se deben superar para que el resultado se considere 'confirmada'."
    )
    required_for_review: int = Field(
        ...,
        description="Cantidad de métodos acumulativos que se deben superar para que el resultado se considere 'a revisar' (debe ser menor que 'required_for_confirmed')."
    )

class VerificationRequest(BaseModel):
    entries: List[Dict[str,Any]] = Field(
        ...,
        description="Lista de entradas ya parseadas (placeholders extraídos). Cada entrada es un diccionario {placeholder: valor}. Esto corresponde al GeneratedResultToVerify."
    )
    process: VerificationProcessRequest = Field(
        ...,
        description="Proceso de verificación (VerificationProcess), que incluye los métodos y los umbrales requeridos."
    )