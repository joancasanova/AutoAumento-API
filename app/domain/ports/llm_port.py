from typing import List

class LLMPort:
    def generate(self, system_prompt: str, user_prompt: str, num_responses:int=1, max_new_tokens:int=100) -> List[str]:
        """Generate text based on prompts."""
        raise NotImplementedError
