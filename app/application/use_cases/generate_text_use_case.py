from typing import List, Dict, Any
from app.domain.entities import GeneratedResult
from app.domain.ports.llm_port import LLMPort

class GenerateTextUseCase:
    def __init__(self, llm: LLMPort):
        self.llm = llm

    def execute(self, system_prompt: str, user_prompt: str, num_return_sequences:int, max_new_tokens:int,
                num_executions:int, reference_data:List[Dict[str,str]]) -> List[GeneratedResult]:
        results = []
        if reference_data:
            for entry in reference_data:
                input_text = entry.get("input","")
                output_text = entry.get("output","")
                prompt = user_prompt.replace("{input}",input_text).replace("{output}",output_text)
                for _ in range(num_executions):
                    responses = self.llm.generate(system_prompt, prompt, num_return_sequences, max_new_tokens)
                    for resp in responses:
                        results.append(GeneratedResult(input_text, resp))
        else:
            # Sin referencia, usar texto genérico
            for _ in range(num_executions):
                prompt = user_prompt.replace("{input}","example_input").replace("{output}","example_output")
                responses = self.llm.generate(system_prompt, prompt, num_return_sequences, max_new_tokens)
                for resp in responses:
                    results.append(GeneratedResult("example_input", resp))

        return results
