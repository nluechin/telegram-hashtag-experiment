# Telegram Hashtag Experiment Bot

This repository contains a Telegram chatbot used for a multi-round hashtag response study.

Participants interact with the bot by submitting short hashtag responses across multiple rounds. The system logs anonymized responses for research analysis.

---

## Features

- Direct message interaction via Telegram bot
- Participant code entry (no personal identifiers stored)
- Multi-round response collection
- Hashtag validation (letters + numbers only)
- CSV data logging (anonymized)

---

## Data Privacy

The bot stores only:

- participant_id
- round_index
- hashtag response
- timestamp
- prompt text

The system **does not store**:
- Telegram usernames
- phone numbers
- chat IDs in analysis data

Telegram is used solely as the interaction interface. All research data are stored locally in CSV format.

---

## Setup

### 1. Install dependencies

### 2. Create `.env` file

### 3. Run the bot

---

## Usage

Participants open the bot and:

1. Enter participant code
2. Submit hashtag responses for each round
3. Data is logged to CSV file

---

## Research Use

This tool is designed for behavioral research and IRB-compliant data collection.

---


