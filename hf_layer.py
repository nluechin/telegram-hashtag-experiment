from transformers import pipeline

''' This is the AI interface logic:

- how to call the model

- how to format the prompt

- how to clean the output

This file creates a small wrapper around a Hugging Face language model.
'''

class HFPipeline:
    def __init__(self, model_name: str = "distilgpt2"):
        self.model_name = model_name
        self.generator = pipeline("text-generation", model=model_name)

    def build_prompt(self, prompt_text: str, human_text: str) -> str:
        return f"{prompt_text}\nHuman: {human_text}\nAI:"

    def generate(self, prompt: str, max_new_tokens: int = 25) -> str:
        result = self.generator(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            num_return_sequences=1,
        )[0]["generated_text"]

        return result.split("AI:", 1)[-1].strip()