# Telegram Bot Setup Guide

This guide explains how to set up, configure, and run the Telegram Hashtag Experiment Bot locally.

## 1. Create a Telegram bot with BotFather

Open Telegram and search for:

```text
@BotFather
```

Start a chat with BotFather and type:

```text
/newbot
```

BotFather will ask for:

- a display name for the bot
- a username for the bot

The username must end in `bot`.

Example:

```text
hashtag_experiment_bot
```

After the bot is created, BotFather will give a bot token.

The token will look something like:

```text
123456789:ABCdefGhIJKlmNoPQRsTUVwxyz
```

Do not share this token publicly.

## 2. Create a `.env` file

In the project folder, create a file named:

```text
.env
```

Inside the `.env` file, add:

```env
TELEGRAM_BOT_TOKEN=your_token_here
```

Replace `your_token_here` with the token from BotFather.

Example:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyz
```

The `.env` file should not be uploaded to GitHub.

## 3. Create a virtual environment

From the project folder, run:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

On Windows, use:

```bash
.venv\Scripts\activate
```

## 4. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

If needed, install the required packages manually:

```bash
pip install python-telegram-bot==21.6 python-dotenv sentence-transformers scikit-learn pandas numpy
```

## 5. Run the bot locally

From the project folder, run:

```bash
python telegram_hashtag_bot.py
```

If the bot starts correctly, the terminal should show:

```text
Bot is running...
```

Keep the terminal window open while testing. If the terminal is closed, the bot will stop responding.

## 6. Open the bot in Telegram

Open Telegram and search for the bot username created through BotFather.

Click the bot and press:

```text
/start
```

The bot should ask for a participant code.

Example:

```text
P001
```

Then the participant can begin submitting hashtag-style responses.

Example:

```text
#grief
```

The bot should respond with a structured system response.

Example:

```text
AI: #pain
```

## 7. Data output

The bot logs responses to a local CSV file.

Default output file:

```text
hashtag_responses.csv
```

This file contains information such as:

- timestamp
- participant_id
- round_idx
- human_raw_text
- human_cleaned_text
- ai_response
- predicted_label
- score_table

This CSV file should not be uploaded to GitHub if it contains study data.

## 8. Troubleshooting

### Bot does not respond in Telegram

Check that:

- the terminal still says `Bot is running...`
- the correct bot token is saved in `.env`
- the `.env` file is in the same project folder
- the bot was started with `/start`

### ModuleNotFoundError

If a package is missing, run:

```bash
pip install -r requirements.txt
```

or install the missing package directly.

Example:

```bash
pip install sentence-transformers
```

### Token error

Check that the `.env` file contains:

```env
TELEGRAM_BOT_TOKEN=your_token_here
```

Make sure there are no quotation marks or extra spaces around the token.

### Bot only works while laptop is open

This is expected when running locally. Local polling requires the computer and terminal to stay running.

For a live study or long-term deployment, the bot should eventually be hosted on a server.

Possible future hosting options include:

- Render
- Railway
- DigitalOcean
- AWS
- Heroku alternatives

## 9. Current system flow

The current bot flow is:

```text
Telegram user message
        ↓
telegram_hashtag_bot.py
        ↓
pipeline.py
        ↓
ml_response_pipeline.py
        ↓
embedding similarity + theme classification
        ↓
structured system response
```

The system currently uses semantic embeddings, cosine similarity, and structured response logic rather than freeform LLM generation.
