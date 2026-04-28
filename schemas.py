"""
schemas.py

Purpose:
Defines standardized data structures for storing participant and AI responses
throughout the experiment pipeline.

This module:
- Creates clean, consistent response objects
- Improves reproducibility and organization
- Simplifies CSV/database logging
- Supports future metadata expansion
- Keeps frontend, backend, and analytics pipelines aligned
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class HumanResponse:
    """
    Stores one participant submission.

    Fields:
    - participant_id: anonymized participant identifier
    - round_idx: current round number
    - raw_text: original participant input
    - cleaned_text: standardized hashtag after preprocessing
    - timestamp: submission time
    - meta: optional expandable metadata
    """
    participant_id: str
    round_idx: int
    raw_text: str
    cleaned_text: str
    timestamp: datetime
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    """
    Stores one AI-generated response.

    Fields:
    - model_name: identifier for current response system
    - prompt: cleaned participant input used by model
    - output_text: selected AI response
    - timestamp: generation time
    - meta: stores prediction metadata (labels, scores, etc.)
    """
    model_name: str
    prompt: str
    output_text: str
    timestamp: datetime
    meta: Dict[str, Any] = field(default_factory=dict)
