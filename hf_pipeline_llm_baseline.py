from transformers import pipeline
import re

"""
Legacy baseline: LLM-based response generator

This module uses a Hugging Face text-generation pipeline to produce
a one-word related response to participant input.

It reflects an earlier version of the project before the system
shifted toward a more controlled embedding-based / ML-driven approach.

Retained for reference and comparison only.
"""

class HFPipeline:
    def __init__(self, model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_name = model_name
        self.generator = pipeline(
            "text-generation",
            model=model_name,
            device=-1
        )

    def build_prompt(self, prompt_text: str, human_text: str) -> str:
        return (
            "Give one related word.\n"
            "Rules: one word only, letters or numbers only, no punctuation, no explanation.\n"
            "Input: yoga\n"
            "Output: balance\n"
            "Input: election\n"
            "Output: politics\n"
            f"Input: {human_text}\n"
            "Output:"
        )

    def generate(self, prompt: str, max_new_tokens: int = 6) -> str:
        result = self.generator(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            num_return_sequences=1,
            return_full_text=False,
        )[0]["generated_text"]

        text = result.strip()

        # keep only first line
        text = text.split("\n", 1)[0].strip()

        # remove common prompt-echo fragments if they appear
        text = text.replace("Output:", "").strip()
        text = text.replace("Input:", "").strip()

        # keep only first word-like chunk
        match = re.search(r"[A-Za-z0-9]+", text)
        if match:
            return match.group(0)

        return "response"
