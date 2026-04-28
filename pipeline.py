from datetime import datetime

from schemas import HumanResponse, AIResponse
from ml_response_pipeline import clean_hashtag, choose_bot_response


MODEL_NAME = "embedding_theme_response_selector"


def run_step(participant_id: str, round_idx: int, raw_text: str):
    cleaned_text = clean_hashtag(raw_text)

    human_response = HumanResponse(
        participant_id=participant_id,
        round_idx=round_idx,
        raw_text=raw_text,
        cleaned_text=cleaned_text,
        timestamp=datetime.now(),
        meta={},
    )

    result = choose_bot_response(cleaned_text)

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

    return human_response, ai_response
