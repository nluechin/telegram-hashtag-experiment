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
    """
    Tracks where one Telegram chat is in the flow.

    participant_id:
      - stored after user enters a valid code (P014)
      - written to CSV (NOT their Telegram info)

    round_idx:
      - which PROMPT index the user is currently on

    awaiting_hashtag:
      - True when we expect a hashtag response
      - False when we expect a participant ID or are transitioning

    withdrawn:
      - user opted out; we stop recording and stop flow
    """
    participant_id: Optional[str] = None
    round_idx: int = 0
    awaiting_hashtag: bool = False
    withdrawn: bool = False

# keyed by telegram chat_id for routing only (NOT written to CSV)
# chat_id is stable within a chat and is how you know "this message belongs to that user session".
user_state: Dict[int, UserState] = {}


# Helpers

def ensure_csv_header(path):
    """
    Creates the CSV file with a header row if it doesn't exist yet.
    This is called right before writing the first row to guarantee structure.
    """
    if os.path.exists(path):
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["unix_time", "participant_id", "round_index", "hashtag", "prompt"])

def normalize_participant_id(text):
    t = (text or "").strip()
    if not t:
        return None
    if not PID_PATTERN.fullmatch(t):
        return None
    t = t.upper()
    if not t.startswith("P"):       #add participant ID to start with "P" 
        t = "P" + t
    return t

def parse_hashtag(text):
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
    # Enforce letters/numbers only
    if not HASHTAG_PATTERN.fullmatch(t):
        return None
    return t

def save_row(participant_id, round_idx, hashtag):
    '''appends one response to the CSV. This writes NO Telegram identifiers.'''
    ensure_csv_header(CSV_PATH)
    prompt_text = PROMPTS[round_idx]        # the prompt shown for this round
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([time.time(), participant_id, round_idx, hashtag, prompt_text])

def get_state(chat_id):
    # If this user does not have a state yet
    if chat_id not in user_state:
        # create a blank state for them
        user_state[chat_id] = UserState()
    return user_state[chat_id]

# Sends the next prompt for the current round OR ends the study if finished
async def send_round_prompt(update, state):
    # If we've already completed all rounds, send the final message and stop expecting input
    if state.round_idx >= len(PROMPTS):
        state.awaiting_hashtag = False
        await update.message.reply_text(DONE_TEXT)
        return

    # select the correct prompt for this round
    prompt = PROMPTS[state.round_idx]
    state.awaiting_hashtag = True       # Mark that the next message we receive should be a hashtag response
    
    # send the prompt message to the user via Telegram
    await update.message.reply_text(f"{prompt}\nReply with a hashtag (example: #breakingnews).")


# Handlers

# /start command: begins the study flow or re-enters the flow without resetting participant_id
async def start_cmd(update, context):
    chat_id = update.effective_chat.id
    state = get_state(chat_id)

    # if they already started and have a PID, prevent re-entry into the study flow
    if state.withdrawn:
        await update.message.reply_text("You previously withdrew. If this is a mistake, contact the research team.")
        return

    # reset progression through rounds while preserving participant_id
    state.round_idx = 0
    state.awaiting_hashtag = False

    # prompt for participant ID (first step of the interaction flow)
    await update.message.reply_text(
        "Welcome. Please enter your participant code to begin (example: P014).\n"
        "Do not enter your name or any personal info."
    )

# /restart command: fully resets participant state and returns to participant ID entry step
async def restart_cmd(update, context):
    chat_id = update.effective_chat.id
    state = get_state(chat_id)

    # If the user has withdrawn, prevent re-entry into the study flow
    if state.withdrawn:
        await update.message.reply_text("You previously withdrew. If this is a mistake, contact the research team.")
        return

    # clear participant identity and reset all progression through rounds
    state.participant_id = None
    state.round_idx = 0
    state.awaiting_hashtag = False

    # prompt for participant ID to begin the study from the start
    await update.message.reply_text(
        "Restarted. Please enter your participant code to begin (example: P014)."
    )

#(COMMENTED OUT FOR PILOT VERSION)
#  /withdraw command: records participant withdrawal and stops all further data collection
# async def withdraw_cmd(update, context):
#    chat_id = update.effective_chat.id
#    state = get_state(chat_id)

#    state.withdrawn = True
#    state.awaiting_hashtag = False

    #clear PID so  stop linking any future inputs
#    state.participant_id = None
#    state.round_idx = 0

#    await update.message.reply_text(
#        "You have withdrawn. No further responses will be recorded. Thank you."
#    )


# Handles all non-command text messages and routes them based on user state
async def message_handler(update, context):
    # ignore updates that are not standard text messages
    if not update.message or not update.message.text:
        return

    # identify chat session and load current participant state
    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    state = get_state(chat_id)

    #(COMMENTED OUT FOR PILOT VERSION)
    #if state.withdrawn:
    #    await update.message.reply_text("You previously withdrew. No responses are being recorded.")
    #    return

    # STEP 1: Collect participant code first
    if state.participant_id is None:
        pid = normalize_participant_id(text)
        # reject invalid participant ID formats
        if pid is None:
            await update.message.reply_text(
                "That does not look like a valid participant code.\n"
                "Please enter something like P014 (letters + numbers only)."
            )
            return

        # store normalized participant ID and begin study flow
        state.participant_id = pid
        await update.message.reply_text(INTRO_TEXT)

        # Send first round prompt and set awaiting_hashtag = True
        await send_round_prompt(update, state)
        return

    # Step 2: Collect hashtag responses
    if state.awaiting_hashtag:
        cleaned = parse_hashtag(text)

        # reject invalid hashtag format
        if cleaned is None:
            await update.message.reply_text(INVALID_HASHTAG_TEXT)
            return

        # write to CSV with participant_id only (no Telegram identifiers)
        save_row(state.participant_id, state.round_idx, cleaned)

        state.round_idx += 1
        state.awaiting_hashtag = False

        # If all rounds are completed, send final message and stop
        if state.round_idx >= len(PROMPTS):
            await update.message.reply_text(DONE_TEXT)
            return

        # Otherwise send next round prompt and continue
        await send_round_prompt(update, state)
        return

    # fallback: if they type randomly, just re-prompt the current round
    await send_round_prompt(update, state)





def main():
    load_dotenv(ENV_PATH)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("restart", restart_cmd))
    #app.add_handler(CommandHandler("withdraw", withdraw_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Telegram Hashtag Bot running...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
