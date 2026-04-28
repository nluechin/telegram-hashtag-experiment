import csv
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from pipeline import run_step


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

DATA_FILE = "hashtag_responses.csv"
MAX_ROUNDS = 10


user_state = {}


def is_valid_hashtag(text: str) -> bool:
    text = text.strip()

    if text.startswith("#"):
        text = text[1:]

    return bool(re.fullmatch(r"[A-Za-z0-9_]+", text))


def clean_display_hashtag(text: str) -> str:
    text = text.strip().lower()

    if text.startswith("#"):
        text = text[1:]

    return text


def initialize_csv():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "timestamp",
                    "participant_id",
                    "round_idx",
                    "human_raw_text",
                    "human_cleaned_text",
                    "ai_response",
                    "predicted_label",
                    "score_table",
                ]
            )


def log_response(human_response, ai_response):
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                datetime.now().isoformat(),
                human_response.participant_id,
                human_response.round_idx,
                human_response.raw_text,
                human_response.cleaned_text,
                ai_response.output_text,
                ai_response.meta.get("predicted_label", ""),
                ai_response.meta.get("score_table", ""),
            ]
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    user_state[chat_id] = {
        "stage": "awaiting_participant_code",
        "participant_id": None,
        "round_idx": 0,
    }

    await update.message.reply_text(
        "Welcome. Please enter your participant code to begin."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message_text = update.message.text.strip()

    if chat_id not in user_state:
        await update.message.reply_text(
            "Please type /start to begin."
        )
        return

    state = user_state[chat_id]

    if state["stage"] == "awaiting_participant_code":
        participant_id = message_text.strip()

        state["participant_id"] = participant_id
        state["stage"] = "in_game"
        state["round_idx"] = 1

        await update.message.reply_text(
            "Thank you. The game will now begin.\n\n"
            "Round 1: Please send one hashtag-style response."
        )
        return

    if state["stage"] == "in_game":
        if not is_valid_hashtag(message_text):
            await update.message.reply_text(
                "Please send one hashtag-style response using only letters, numbers, or underscores. Example: #grief"
            )
            return

        participant_id = state["participant_id"]
        round_idx = state["round_idx"]

        human_response, ai_response = run_step(
            participant_id=participant_id,
            round_idx=round_idx,
            raw_text=message_text,
        )

        log_response(human_response, ai_response)

        await update.message.reply_text(
            f"AI: #{ai_response.output_text}"
        )

        if round_idx >= MAX_ROUNDS:
            state["stage"] = "complete"

            await update.message.reply_text(
                "Thank you. The activity is now complete."
            )
            return

        state["round_idx"] += 1

        await update.message.reply_text(
            f"Round {state['round_idx']}: Please send your next hashtag-style response."
        )
        return

    if state["stage"] == "complete":
        await update.message.reply_text(
            "You have already completed the activity. Thank you."
        )


def main():
    initialize_csv()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
