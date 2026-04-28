from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class HumanResponse:
    participant_id: str
    round_idx: int
    raw_text: str
    cleaned_text: str
    timestamp: datetime
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    model_name: str
    prompt: str
    output_text: str
    timestamp: datetime
    meta: Dict[str, Any] = field(default_factory=dict)
