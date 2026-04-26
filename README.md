# Telegram Hashtag Experiment Bot

This repository contains a Telegram-based chatbot used to run a multi-round experiment on how people generate and align meaning through interaction with a machine learning system.

The chatbot itself and its interaction flow are mostly set, but the exact research focus is still evolving and may shift over time. In general, the project is centered on understanding human–AI interaction, especially how meaning develops across multiple rounds of exchange.

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

### 1. Install dependencies (hugging face)

### 2. Create `.env` file (for telegram bot token)

### 3. Run the bot locally

---

## Usage

Participants open the bot by clicking a link and:

1. Enter participant code
2. Submit hashtag responses for each round
3. Data is logged to CSV file

---

## Project Evolution

In the early stages of this project we tried building a chatbot using Slack as the software platform but it posed IRB concerns such as 2FA and other privacy concerns. After realizing these issues we proceeded by switching software platforms to telegram, another messaging app.

Upon switching to telegram I reprogrammed and setup a chatbot using the telegram API. This project originally used a lightweight LLM-based response generator (`TinyLlama`) to produce one related word in response to participant hashtags. That version served as an early prototype for testing interactive human–AI flow inside Telegram.

As the project evolved, the response-generation approach shifted toward a more controlled semantic pipeline based on embeddings, cosine similarity, and structured machine learning logic. This change was made to improve:

- consistency of responses
- interpretability of outputs
- reproducibility of experimental behavior
- alignment with downstream analysis methods

The earlier LLM-based implementation is retained in the repository as a baseline/reference point, but it is no longer the primary experimental direction. The semantic pipeline is in this repo titled semantic_pipeline_v1.ipynb is something I explored to improve the chat bot responses but as a forewarning there may be some mistakes in it, and has not yet been reviewed by my mentor Dr. Hunter P.

---

## Research Use

This tool is built off of Hunter Priniski's Otree Network experiments (link: https://github.com/jpriniski/NetCom/tree/main/Experiment%20Software) and designed for researchf studies of human–AI interaction, language, and meaning formation.
---

Version 20+ of python-telegram-bot is built on asyncio, which is Python’s system for:

handling many tasks at once

without using threads

very efficient for network-heavy apps (like bots)
