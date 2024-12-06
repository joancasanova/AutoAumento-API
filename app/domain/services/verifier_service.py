from typing import List
from app.domain.entities import GeneratedResult

class VerifierService:
    def __init__(self, threshold:float=0.9, upper_threshold:float=0.995, positive_responses:List[str]=["Sí","sí","yes"], num_ok:int=4):
        self.threshold = threshold
        self.upper_threshold = upper_threshold
        self.positive_responses = positive_responses
        self.num_ok = num_ok

    def verify_embedding(self, similarity: float) -> bool:
        # Si es muy similar (>= upper_threshold) se considera idéntico => False
        if similarity >= self.upper_threshold:
            return False
        return self.threshold < similarity < self.upper_threshold

    def verify_consensus(self, responses: List[str]) -> bool:
        # Contar cuántas respuestas contienen una respuesta positiva
        num_pos = sum(any(p.lower() in (r or "").lower() for p in self.positive_responses) for r in responses)
        return num_pos >= self.num_ok

    def decide_verdict(self, conditions_met: int, total_conditions: int) -> int:
        # 0 (confirmada), 1 (a revisar), -1 (fallido)
        if total_conditions == 0:
            return -1
        if conditions_met == total_conditions:
            return 0
        elif conditions_met == total_conditions - 1:
            return 1
        else:
            return -1
