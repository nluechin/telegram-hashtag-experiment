import random
import re
from typing import Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


theme_anchors: Dict[str, str] = {
    "patient_autonomy": "choice consent control personal decision rights autonomy",
    "medical_ethics": "ethics care harm responsibility medicine treatment trust",
    "fairness_rationing": "fairness scarcity resources rationing access equality",
    "trauma_emotion": "pain grief fear sadness trauma healing emotion",
    "competition_status": "winning losing status rivalry competition power",
    "deception_trust": "lying deception honesty betrayal trust truth",
    "media_public_reaction": "public attention media scandal reaction outrage news",
}


response_bank: Dict[str, List[str]] = {
    "patient_autonomy": [
        "choice",
        "consent",
        "rights",
        "control",
        "decision",
    ],
    "medical_ethics": [
        "care",
        "ethics",
        "trust",
        "harm",
        "treatment",
    ],
    "fairness_rationing": [
        "fairness",
        "scarcity",
        "access",
        "resources",
        "equity",
    ],
    "trauma_emotion": [
        "pain",
        "grief",
        "healing",
        "fear",
        "loss",
    ],
    "competition_status": [
        "winning",
        "status",
        "rivalry",
        "power",
        "score",
    ],
    "deception_trust": [
        "truth",
        "trust",
        "betrayal",
        "honesty",
        "deception",
    ],
    "media_public_reaction": [
        "public",
        "media",
        "reaction",
        "attention",
        "outrage",
    ],
}


anchor_names = list(theme_anchors.keys())
anchor_texts = list(theme_anchors.values())
anchor_embeddings = embedding_model.encode(anchor_texts)


def clean_hashtag(text: str) -> str:
    text = text.strip().lower()
    text = text.replace("#", "")
    text = re.sub(r"[^a-z0-9_]", "", text)
    return text


def choose_bot_response(user_hashtag: str) -> Dict:
    cleaned_input = clean_hashtag(user_hashtag)

    if cleaned_input == "":
        return {
            "input": user_hashtag,
            "cleaned_input": cleaned_input,
            "predicted_label": "invalid",
            "response": "tryagain",
            "score_table": [],
        }

    user_embedding = embedding_model.encode([cleaned_input])

    similarities = cosine_similarity(user_embedding, anchor_embeddings)[0]

    best_idx = int(np.argmax(similarities))
    predicted_label = anchor_names[best_idx]

    response = random.choice(response_bank[predicted_label])

    score_table = [
        {
            "label": anchor_names[i],
            "cosine_similarity": float(similarities[i]),
        }
        for i in range(len(anchor_names))
    ]

    score_table = sorted(
        score_table,
        key=lambda row: row["cosine_similarity"],
        reverse=True,
    )

    return {
        "input": user_hashtag,
        "cleaned_input": cleaned_input,
        "predicted_label": predicted_label,
        "response": response,
        "score_table": score_table,
    }
