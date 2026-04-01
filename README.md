# Telegram Hashtag Experiment Bot

This repository contains a Telegram-based chatbot used to run a multi-round experiment on how people generate and align meaning through interaction with a machine learning system.

Participants interact with the bot by submitting hashtag responses and receiving system-generated responses across multiple rounds. The experiment is designed to study how meanings evolve through human–AI interaction.

---
## Overview
The system enables a structured interaction between participants and an automated agent.

Each participant:

interacts with the bot via direct message
enters a unique participant code
submits one hashtag per round
receives a generated response from the system

This creates a feedback loop where both human and system responses influence subsequent behavior.

---
## Features

- Telegram bot interface (DM-based interaction)
- Participant code entry (no personal identifiers required)
- Multi-round interactive flow (human ↔ system)
- Hashtag validation and formatting
- Structured CSV logging
- Integration with semantic analysis pipeline

---

## Data Privacy

The bot stores only:

- participant_id
- round_index
- hashtag response
- system outputs
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

This tool is designed for behavioral and computational social science research, including studies of human–AI interaction, language, and meaning formation.
---

Version 20+ of python-telegram-bot is built on asyncio, which is Python’s system for:

handling many tasks at once

without using threads

very efficient for network-heavy apps (like bots)
