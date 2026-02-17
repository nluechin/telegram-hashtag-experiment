import os
import csv
import time
import re
from dataclasses import dataclass
from typing import Dict, Optional

from dotenv import load_dotenv
from telegram import Update     #telegram library objects: Update is object representing an incoming event (message, command, etc.)
# telegram.ext provides the bot "framework" (app + handlers + filters)
from telegram.ext import (
    Application,                # the main bot application (dispatcher + HTTP client)
    CommandHandler,             # routes /start, /restart, /withdraw
    MessageHandler,             # routes non-command text messages
    ContextTypes,               # type hints for callback context
    filters,                    # prebuilt filters for matching messages
)


ENV_PATH = ".env"
CSV_PATH = "Hashtag_telegram_study.csv"

INTRO_TEXT = "Starting the game now."
DONE_TEXT = "All done. Thank you!"
INVALID_HASHTAG_TEXT = (
    "Please reply with a single hashtag-style word using only letters and numbers.\n"
    "No spaces. Example: #breakingnews"
)

# Customize rounds here
PROMPTS = [
    "Please submit a short hashtag response.",
    "Please submit another short hashtag response.",
    "Please submit another short hashtag response.",
]

# Participant code format
# Examples accepted: P014, p014, 014 
# - accepts "P014", "p014", or "014"
# - 2 to 4 digits (so 01..9999), optional leading P
PID_PATTERN = re.compile(r"^P?\d{2,4}$", re.IGNORECASE)

# Hashtag content pattern:
# - after stripping leading '#', must be letters/numbers only
# - no underscores, hyphens, emojis, punctuation, etc.
HASHTAG_PATTERN = re.compile(r"^[A-Za-z0-9]+$")


# State (in-memory)

@dataclass
class UserState:
    participant_id: Optional[str] = None
    round_idx: int = 0
    awaiting_hashtag: bool = False
    withdrawn: bool = False

# Keyed by Telegram chat_id for routing only (NOT written to CSV)
user_state: Dict[int, UserState] = {}


# Helpers

def ensure_csv_header(path: str) -> None:
    if os.path.exists(path):
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["unix_time", "participant_id", "round_index", "hashtag", "prompt"])

def normalize_participant_id(text: str) -> Optional[str]:
    t = (text or "").strip()
    if not t:
        return None
    if not PID_PATTERN.fullmatch(t):
        return None
    t = t.upper()
    if not t.startswith("P"):
        t = "P" + t
    return t

def parse_hashtag(text: str) -> Optional[str]:
    if not text:
        return None
    t = text.strip()
    if not t:
        return None
    # remove leading #
    if t.startswith("#"):
        t = t[1:]
    # no spaces
    if " " in t:
        return None
    if not HASHTAG_PATTERN.fullmatch(t):
        return None
    return t

def save_row(participant_id: str, round_idx: int, hashtag: str) -> None:
    ensure_csv_header(CSV_PATH)
    prompt_text = PROMPTS[round_idx]
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([time.time(), participant_id, round_idx, hashtag, prompt_text])

def get_state(chat_id: int) -> UserState:
    if chat_id not in user_state:
        user_state[chat_id] = UserState()
    return user_state[chat_id]

async def send_round_prompt(update: Update, state: UserState) -> None:
    if state.round_idx >= len(PROMPTS):
        state.awaiting_hashtag = False
        await update.message.reply_text(DONE_TEXT)
        return

    prompt = PROMPTS[state.round_idx]
    state.awaiting_hashtag = True
    await update.message.reply_text(f"{prompt}\nReply with a hashtag (example: #breakingnews).")

# -----------------------------
# Handlers
# -----------------------------
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    state = get_state(chat_id)

    # If they already started and have a PID, you can decide whether to continue or restart
    if state.withdrawn:
        await update.message.reply_text("You previously withdrew. If this is a mistake, contact the research team.")
        return

    # Reset only the flow, not the participant_id, unless you want /restart for full reset
    state.round_idx = 0
    state.awaiting_hashtag = False

    await update.message.reply_text(
        "Welcome. Please enter your participant code to begin (example: P014).\n"
        "Do not enter your name or any personal info."
    )

async def restart_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    state = get_state(chat_id)

    if state.withdrawn:
        await update.message.reply_text("You previously withdrew. If this is a mistake, contact the research team.")
        return

    state.participant_id = None
    state.round_idx = 0
    state.awaiting_hashtag = False

    await update.message.reply_text(
        "Restarted. Please enter your participant code to begin (example: P014)."
    )

async def withdraw_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    state = get_state(chat_id)

    state.withdrawn = True
    state.awaiting_hashtag = False

    # Optional: clear PID so you stop linking any future inputs
    state.participant_id = None
    state.round_idx = 0

    await update.message.reply_text(
        "You have withdrawn. No further responses will be recorded. Thank you."
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    state = get_state(chat_id)

    if state.withdrawn:
        await update.message.reply_text("You previously withdrew. No responses are being recorded.")
        return

    # Step 1: Collect participant code first
    if state.participant_id is None:
        pid = normalize_participant_id(text)
        if pid is None:
            await update.message.reply_text(
                "That does not look like a valid participant code.\n"
                "Please enter something like P014 (letters + numbers only)."
            )
            return

        state.participant_id = pid
        await update.message.reply_text(INTRO_TEXT)
        await send_round_prompt(update, state)
        return

    # Step 2: Collect hashtag responses
    if state.awaiting_hashtag:
        cleaned = parse_hashtag(text)
        if cleaned is None:
            await update.message.reply_text(INVALID_HASHTAG_TEXT)
            return

        # Write to CSV with participant_id only (no Telegram identifiers)
        save_row(state.participant_id, state.round_idx, cleaned)

        state.round_idx += 1
        state.awaiting_hashtag = False

        if state.round_idx >= len(PROMPTS):
            await update.message.reply_text(DONE_TEXT)
            return

        await send_round_prompt(update, state)
        return

    # Fallback: if they type randomly, just re-prompt the current round
    await send_round_prompt(update, state)

# -----------------------------
# Run
# -----------------------------
def main() -> None:
    load_dotenv(ENV_PATH)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("restart", restart_cmd))
    app.add_handler(CommandHandler("withdraw", withdraw_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Telegram Hashtag Bot running...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
