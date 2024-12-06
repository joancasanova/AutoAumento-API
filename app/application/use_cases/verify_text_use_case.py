from typing import List, Dict
from app.domain.entities import GeneratedResult, VerificationPrompt
from app.domain.ports.llm_port import LLMPort
from app.domain.ports.embeddings_port import EmbeddingsPort
from app.domain.services.verifier_service import VerifierService

class VerifyTextUseCase:
    def __init__(self, llm: LLMPort, embedder: EmbeddingsPort, verifier_service: VerifierService):
        self.llm = llm
        self.embedder = embedder
        self.verifier_service = verifier_service

    def execute(self, verification_prompts: List[VerificationPrompt], generated_results: List[GeneratedResult]) -> List[GeneratedResult]:
        # Determinar el método (embedding, consensus, all, None) a partir del primer prompt
        verification_method = "all"
        if verification_prompts:
            candidate = verification_prompts[0].name.lower()
            if candidate in ["embedding","consensus","all","none"]:
                verification_method = candidate

        for res in generated_results:
            input_text = res.input
            output_text = res.output

            methods = []
            if verification_method == "all":
                methods = ["embedding", "consensus"]
            elif verification_method in ["embedding", "consensus"]:
                methods = [verification_method]
            elif verification_method == "none":
                methods = []

            conditions_met = 0
            total_conditions = 0

            # Embedding check
            if "embedding" in methods:
                total_conditions += 1
                similarity = self.embedder.get_similarity(input_text, output_text)
                if self.verifier_service.verify_embedding(similarity):
                    conditions_met += 1
                else:
                    # Si falla embedding, no seguimos
                    verdict = self.verifier_service.decide_verdict(conditions_met, total_conditions)
                    self._apply_verdict(res, verdict)
                    continue

            # Consensus check
            if "consensus" in methods:
                total_conditions += 1
                # Usar el primer prompt de verificación para consenso, por ejemplo
                # Generamos respuestas con el LLM
                if verification_prompts:
                    vp = verification_prompts[0]
                    # Combinar context + instruction
                    combined_system = vp.context
                    combined_user = vp.instruction.replace("{input}", input_text).replace("{output}", output_text)
                    responses = self.llm.generate(combined_system, combined_user, vp.num_return_sequences, vp.max_new_tokens)
                    if self.verifier_service.verify_consensus(responses):
                        conditions_met += 1

            verdict = self.verifier_service.decide_verdict(conditions_met, total_conditions)
            self._apply_verdict(res, verdict)

        return generated_results

    def _apply_verdict(self, result: GeneratedResult, verdict: int):
        if verdict == 0:
            result.verification_status = "confirmada"
        elif verdict == 1:
            result.verification_status = "a revisar"
        else:
            result.verification_status = "fallido"
