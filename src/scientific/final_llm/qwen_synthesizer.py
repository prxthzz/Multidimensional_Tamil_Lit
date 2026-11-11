from typing import Any, Dict

import torch

from scientific.final_llm.interface import FinalLLMInterface
from scientific.final_llm.parser import FinalLLMParser
from scientific.final_llm.prompt import build_final_prompt


class QwenFinalSynthesizer(FinalLLMInterface):
    """
    Final response synthesizer using Qwen.

    The Final LLM explains the structured AnalysisResult.
    It does not determine relationships or create evidence.
    """

    def __init__(self, qwen_model):
        self.qwen_model = qwen_model
        self.parser = FinalLLMParser()

    def synthesize(
        self,
        analysis_result: Dict[str, Any],
    ) -> Dict[str, Any]:

        prompt = build_final_prompt(
            analysis_result
        )

        # Test/dummy model support.
        # A fake model may implement interpret() directly.
        if hasattr(
            self.qwen_model,
            "interpret",
        ):
            result = self.qwen_model.interpret(
                {
                    "analysis_result": analysis_result,
                    "final_prompt": prompt,
                }
            )

            response = result.get(
                "response",
                result.get(
                    "interpretation_notes",
                    "",
                ),
            )

            return self.parser.parse(
                response
            )

        # Real QwenTinyLLM support.
        tokenizer = self.qwen_model.tokenizer
        model = self.qwen_model.model

        messages = [
            {
                "role": "system",
                "content": (
                    "You are the final explanation layer "
                    "of a scientific-literary knowledge "
                    "system. Only explain the supplied "
                    "structured analysis. Never invent "
                    "evidence or relationships."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = tokenizer(
            text,
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False,
            )

        generated_tokens = outputs[
            0
        ][inputs["input_ids"].shape[1]:]

        response = tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        )

        return self.parser.parse(
            response
        )