import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List
from app.domain.ports.llm_port import LLMPort

class InstructModel(LLMPort):
    def __init__(self, model_name: str = "EleutherAI/gpt-neo-125M"):
        print(f"Loading LLM model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def generate(self, system_prompt: str, user_prompt: str, num_responses:int=1, max_new_tokens:int=100) -> List[str]:
        full_prompt = f"{system_prompt}\n{user_prompt}"
        inputs = self.tokenizer([full_prompt], return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            num_return_sequences=num_responses,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
