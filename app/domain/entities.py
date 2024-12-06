from typing import List, Dict, Optional, Any

class GeneratedResult:
    def __init__(self, input_text: str, output_text: str):
        self.input = input_text
        self.output = output_text
        self.verification_status: Optional[str] = None  # "confirmada", "a revisar", "fallido"

class VerificationPrompt:
    def __init__(self, name: str, context: str, instruction: str,
                 num_return_sequences:int, max_new_tokens:int, num_positive:int, positive_responses:List[str]):
        self.name = name
        self.context = context
        self.instruction = instruction
        self.num_return_sequences = num_return_sequences
        self.max_new_tokens = max_new_tokens
        self.num_positive = num_positive
        self.positive_responses = positive_responses

class SetupData:
    def __init__(self, model:str, generation_prompts:Dict[str,Any],
                 verification_prompts:List[Dict[str,Any]], reference_data:List[Dict[str,str]]):
        self.model = model
        self.generation_prompts = generation_prompts
        self.verification_prompts = verification_prompts
        self.reference_data = reference_data
