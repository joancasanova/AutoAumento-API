# llm_service.py
from app.infrastructure.llm.instruct_model import InstructModel
from app.domain.ports.llm_port import LLMPort

def get_llm(model_name:str="EleutherAI/gpt-neo-125M") -> LLMPort:
    # Podrías usar un caché aquí si lo deseas
    return InstructModel(model_name)
