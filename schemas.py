from dataclasses import dataclass
from typing import Dict, Any

#@dataclass automatically implements the init, repr, eq methods. defined in the data class are called fields/ attributes (not keys)
@dataclass
class HumanResponse:
    participant_id: str
    round_idx: int
    raw_text: str
    cleaned_text: str
    timestamp: float
    meta: Dict[str, Any] #extra info (like source, model, etc.)

#example response object:
#human = HumanResponse(
#    participant_id="P014",
#    round_idx=0,
#    raw_text="#breakingnews",
#    cleaned_text="breakingnews",
#    timestamp=1710000000.0,
#    meta={"source": "telegram"}
#)

@dataclass
class AIResponse:
    model_name: str
    prompt: str
    output_text: str
    timestamp: float
    meta: Dict[str, Any]

#example response object:
#ai = AIResponse(
#    model_name="distilgpt2",
#    prompt=prompt,
#    output_text="financialcrisis",
#    timestamp=time.time(),
#    meta={
#        "max_tokens": 25,
#        "temperature": 0.8
#    }
#)