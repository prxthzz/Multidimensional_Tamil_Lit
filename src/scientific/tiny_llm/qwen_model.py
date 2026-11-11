from typing import Any, Dict

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scientific.tiny_llm.interface import TinyLLMInterface
from scientific.tiny_llm.parser import TinyLLMOutputParser
from scientific.tiny_llm.prompt import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)


class QwenTinyLLM(TinyLLMInterface):
    """
    Qwen2.5-0.5B-Instruct implementation of the TinyLLMInterface.

    CPU-oriented implementation for the scientific branch.
    """

    MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.MODEL_NAME,
            dtype=torch.float32,
        )

        self.model.eval()

        self.parser = TinyLLMOutputParser()

    def interpret(
        self,
        scientific_query: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate and parse a scientific semantic interpretation.
        """

        prompt = USER_PROMPT_TEMPLATE.format(
            scientific_query=scientific_query
        )

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False,
            )

        generated_tokens = outputs[
            0
        ][inputs["input_ids"].shape[1]:]

        raw_response = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        )

        return self.parser.parse(raw_response)