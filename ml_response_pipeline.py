import random
import re
from typing import Dict, List

# Import NumPy.
# Used here for selecting the highest similarity score.
import numpy as np

# Import SentenceTransformer.
# This model converts words or short phrases into embedding vectors,
# allowing semantic comparison beyond exact word matching.
from sentence_transformers import SentenceTransformer

# Import cosine similarity function.
# Cosine similarity compares semantic closeness between embeddings.
from sklearn.metrics.pairwise import cosine_similarity


# Name of the embedding model used.
# all-MiniLM-L6-v2 is lightweight, fast, and effective for short semantic inputs.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# Load the embedding model once at script startup.
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


# NOTE:
# response bank candidates were scaffolded with ChatGPT.
#
# These outputs were then manually reviewed.
#
# 
# The system is deterministic and uses embedding similarity
# plus controlled category selection, rather than unconstrained LLM generation.


# Theme anchors:
# Each category represents a broader semantic narrative domain.
# Anchor text serves as the semantic prototype for that category.
theme_anchors: Dict[str, str] = {
    "patient_autonomy": "choice consent control personal decision rights autonomy",
    "medical_ethics": "ethics care harm responsibility medicine treatment trust",
    "fairness_rationing": "fairness scarcity resources rationing access equality",
    "trauma_emotion": "pain grief fear sadness trauma healing emotion",
    "competition_status": "winning losing status rivalry competition power",
    "deception_trust": "lying deception honesty betrayal trust truth",
    "media_public_reaction": "public attention media scandal reaction outrage news",
}


# Controlled response bank:
# Each category contains short, experimentally constrained response terms.
#
# The bot selects from these predefined terms instead of generating open text.
# This design improves:
# - Predictability
# - Experimental consistency
# - Ease of interpretation
# - Reduced risk of nonsensical outputs
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


# Store theme names separately for label lookup.
anchor_names = list(theme_anchors.keys())


# Store anchor texts separately for embedding generation.
anchor_texts = list(theme_anchors.values())


# Precompute anchor embeddings.
# This is done once for efficiency.
anchor_embeddings = embedding_model.encode(anchor_texts)


def clean_hashtag(text: str) -> str:

    # Standardize spacing and capitalization
    text = text.strip().lower()

    # Remove hashtag symbol
    text = text.replace("#", "")

    # Remove unwanted characters
    text = re.sub(r"[^a-z0-9_]", "", text)

    return text


def choose_bot_response(user_hashtag: str) -> Dict:
    """
    Process participant hashtag and choose a semantically aligned bot response.

    1. Clean user input
    2. Embed cleaned hashtag
    3. Compare against theme anchors
    4. Predict best category
    5. Randomly choose controlled response from category bank
    6. Return full decision metadata

    Parameters:
        user_hashtag (str): Raw participant hashtag

    Returns:
        Dict:
            - input
            - cleaned_input
            - predicted_label
            - response
            - score_table
    """

    # Clean participant input
    cleaned_input = clean_hashtag(user_hashtag)

    # Handle invalid or empty submissions
    if cleaned_input == "":
        return {
            "input": user_hashtag,
            "cleaned_input": cleaned_input,
            "predicted_label": "invalid",
            "response": "tryagain",
            "score_table": [],
        }

    # Convert cleaned hashtag into semantic embedding
    user_embedding = embedding_model.encode([cleaned_input])

    # Compare user embedding to all anchor embeddings
    similarities = cosine_similarity(user_embedding, anchor_embeddings)[0]

    # Select most semantically similar category
    best_idx = int(np.argmax(similarities))

    # Retrieve category label
    predicted_label = anchor_names[best_idx]

    # Choose one response from that category's controlled bank
    response = random.choice(response_bank[predicted_label])

    # Build interpretability table showing similarity scores for all categories
    score_table = [
        {
            "label": anchor_names[i],
            "cosine_similarity": float(similarities[i]),
        }
        for i in range(len(anchor_names))
    ]

    # Sort scores descending for easier debugging and presentation
    score_table = sorted(
        score_table,
        key=lambda row: row["cosine_similarity"],
        reverse=True,
    )

    # Return full system output
    return {
        "input": user_hashtag,
        "cleaned_input": cleaned_input,
        "predicted_label": predicted_label,
        "response": response,
        "score_table": score_table,
    }
