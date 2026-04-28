"""
pipeline.py

Purpose:
Central orchestration layer for one full participant → AI interaction cycle.

This module:
- Cleans participant hashtag input
- Structures and stores participant response data
- Passes cleaned input into the ML response system
- Generates controlled AI responses
- Structures AI output with metadata
- Returns both responses for logging, display, or analysis

Why this file matters:
- Separates experiment logic from Telegram/frontend code
- Makes model swapping easier without changing bot infrastructure
- Standardizes response flow for reproducibility
- Simplifies future handoff, debugging, and server deployment
"""

from datetime import datetime

# Standardized schemas for structured human + AI response logging
from schemas import HumanResponse, AIResponse

# Core ML response pipeline functions
from ml_response_pipeline import clean_hashtag, choose_bot_response


# Current model/system identifier
MODEL_NAME = "embedding_theme_response_selector"


def run_step(participant_id: str, round_idx: int, raw_text: str):
    """
    Executes one full participant interaction step.
    """

    # Clean raw participant input for consistent processing
    cleaned_text = clean_hashtag(raw_text)

    # Build structured participant response object
    human_response = HumanResponse(
        participant_id=participant_id,
        round_idx=round_idx,
        raw_text=raw_text,
        cleaned_text=cleaned_text,
        timestamp=datetime.now(),
        meta={},
    )

    # Generate AI response using embedding + theme pipeline
    result = choose_bot_response(cleaned_text)

    # Build structured AI response object
    ai_response = AIResponse(
        model_name=MODEL_NAME,
        prompt=cleaned_text,
        output_text=result["response"],
        timestamp=datetime.now(),
        meta={
            "predicted_label": result["predicted_label"],
            "score_table": result["score_table"],
        },
    )

    # Return both outputs
    return human_response, ai_response
