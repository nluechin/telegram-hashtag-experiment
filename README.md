# Telegram Hashtag Experiment Bot

This repository contains a Telegram-based chatbot used to run a multi-round experiment on how people generate and align meaning through interaction with a machine learning system.

The chatbot itself and its interaction flow are mostly set, but the exact research focus is still evolving and may shift over time. In general, the project is centered on understanding human-AI interaction, especially how meaning develops across multiple rounds of exchange.

## Overview

The system enables a structured interaction between participants and an automated agent.

Each participant:

- interacts with the bot via direct message
- enters a unique participant code
- submits one hashtag per round
- receives a generated response from the system

This creates a feedback loop where both human and system responses influence subsequent behavior.

## Features

- Telegram bot interface, DM-based interaction
- Participant code entry, no personal identifiers required
- Multi-round interactive flow, human to system
- Hashtag validation and formatting
- Structured CSV logging
- Integration with semantic analysis pipeline
- Embedding-based semantic classification
- Theme prediction through cosine similarity and structured machine learning logic
- Controlled system response generation for improved consistency and interpretability

## Data Privacy

The bot stores only:

- participant_id
- round_index
- hashtag response
- system outputs
- timestamp
- prompt text

The system does not store:

- Telegram usernames
- phone numbers
- chat IDs in analysis data

Telegram is used solely as the interaction interface. All research data are stored locally in CSV format.

## Setup

### 1. Install dependencies

python-telegram-bot==21.6  
python-dotenv  
sentence-transformers  
scikit-learn  
pandas  
numpy  

### 2. Create `.env` file for Telegram bot token

### 3. Run the bot locally

## Usage

Participants open the bot by clicking a link and:

- enter participant code
- submit hashtag responses for each round
- receive structured machine learning system responses
- data is logged to CSV file

## Project Evolution

In the early stages of this project we tried building a chatbot using Slack as the software platform but it posed IRB concerns such as 2FA and other privacy concerns. After realizing these issues we proceeded by switching software platforms to Telegram, another messaging app.

Upon switching to Telegram I reprogrammed and setup a chatbot using the Telegram API. This project originally used a lightweight LLM-based response generator, TinyLlama, to produce one related word in response to participant hashtags. That version served as an early prototype for testing interactive human-AI flow inside Telegram.

As the project evolved, the response-generation approach shifted toward a more controlled semantic pipeline based on embeddings, cosine similarity, theme classification, and structured machine learning logic. This change was made to improve:

- consistency of responses
- interpretability of outputs
- reproducibility of experimental behavior
- alignment with downstream analysis methods

The earlier LLM-based implementation may remain in earlier commits or as reference material, but the current primary experimental direction is the semantic ML pipeline.

The semantic pipeline in this repo, titled `semantic_pipeline_v1.ipynb`, reflects exploratory work used to improve chatbot response architecture, though it may still contain mistakes and has not yet been fully reviewed by my mentor Dr. Hunter P.

## File Map

```text
telegram_hashtag_bot.py       Main Telegram interface and participant flow
pipeline.py                   Connects bot input to the response logic
ml_response_pipeline.py       Semantic/theme-based response selector
schemas.py                    Data structures for human and system responses
requirements.txt              Python dependencies
semantic_pipeline_v1.ipynb    Exploratory notebook for semantic response development
SETUP_GUIDE.md                Instructions for configuring and running the Telegram bot
NOTES_FOR_HANDOFF.md          Project status, transfer notes, and future recommendations
```

## Current Limitations

The current response system is still a prototype and should be reviewed before being used in a live research study.

The semantic response pipeline is intended to improve consistency, interpretability, and reproducibility, but it may still need additional testing, review, and adjustment.

The current system uses structured response logic instead of freeform LLM generation. This means the bot responses are more controlled, but also less flexible than a fully generative chatbot.

## IRB and Research Use Note

This repository is a technical prototype. Any live participant use should follow the approved IRB protocol, consent language, and data handling requirements.

Telegram is used only as the participant-facing interaction interface. Research data should be reviewed and stored according to the study protocol.

## Example Interaction

```text
Bot: Welcome. Please enter your participant code to begin.

User: P001

Bot: Thank you. The game will now begin.
Round 1: Please send one hashtag-style response.

User: #grief

Bot: AI: #pain

Bot: Round 2: Please send your next hashtag-style response.
```

## Research Use

This tool is built off of Hunter Priniski's Otree Network experiments.

Link: https://github.com/jpriniski/NetCom/tree/main/Experiment%20Software

It is designed for research studies of human-AI interaction, language, and meaning formation.

Version 20+ of `python-telegram-bot` is built on asyncio, which is Python's system for:

- handling many tasks at once
- operating without threads
- efficiently supporting network-heavy applications like bots
