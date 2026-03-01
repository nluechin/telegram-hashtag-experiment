import time
from schemas import HumanResponse, AIResponse

''' This is the experiment design logic:

-  how rounds work

- how human + AI interact

- what gets logged

- what the prompt is
'''
def run_step(hf, participant_id, round_idx, raw_text, cleaned_text, prompt_text):
    human = HumanResponse(
        participant_id=participant_id,
        round_idx=round_idx,
        raw_text=raw_text,
        cleaned_text=cleaned_text,
        timestamp=time.time(),
        meta={"source": "telegram"},
    )

    model_prompt = hf.build_prompt(prompt_text, cleaned_text)
    ai_text = hf.generate(model_prompt, max_new_tokens=25)

    ai = AIResponse(
        model_name=hf.model_name,
        prompt=model_prompt,
        output_text=ai_text,
        timestamp=time.time(),
        meta={"max_new_tokens": 25},
    )

    return human, ai