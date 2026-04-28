# Notes for Handoff

This document summarizes the current status of the Telegram Hashtag Experiment Bot for anyone reviewing, testing, or continuing the project.

## Current Status

The Telegram bot is currently able to:

- start a direct message interaction with a participant
- ask for a participant code
- run a multi-round hashtag interaction
- validate hashtag-style responses
- generate structured system responses
- log interaction data to a local CSV file

The chatbot interaction flow is mostly set, but the exact research focus and final experimental framing may continue to evolve.

## Current Response System

The current system uses a semantic machine learning response pipeline rather than freeform LLM generation.

The flow is:

```text
participant hashtag
        ↓
cleaned text
        ↓
semantic embedding
        ↓
similarity to theme anchors
        ↓
predicted theme
        ↓
structured system response
```

The main response logic is located in:

```text
ml_response_pipeline.py
```

The Telegram bot calls this logic through:

```text
pipeline.py
```

## Important Files

```text
telegram_hashtag_bot.py       Runs the Telegram bot and handles participant interaction
pipeline.py                   Connects Telegram input to the response pipeline
ml_response_pipeline.py       Contains semantic classification and response selection logic
schemas.py                    Defines HumanResponse and AIResponse data structures
requirements.txt              Lists required Python packages
semantic_pipeline_v1.ipynb    Exploratory notebook for developing the semantic pipeline
SETUP_GUIDE.md                Explains how to configure and run the bot locally
README.md                     Main project overview and research context
```

## What Works

Currently working:

- Telegram bot setup through BotFather token
- local bot execution through `telegram_hashtag_bot.py`
- participant code entry
- hashtag validation
- multi-round interaction structure
- structured response generation
- CSV logging

## What Needs Review

The following should be reviewed before live participant use:

- semantic theme categories
- response bank wording
- number of rounds
- CSV fields
- IRB and consent language
- privacy and data handling details
- whether the response behavior properly aligns with the final research question
- server deployment considerations

## Research and IRB Notes

This repository is a technical prototype. Any live participant use should follow the approved IRB protocol, consent form, and study procedures.

The bot is designed to avoid storing unnecessary personal identifiers. Telegram is used as the interaction interface, while the research data are stored locally in CSV format.

All future study deployment should be reviewed for:

- participant privacy
- consent clarity
- platform compliance
- server security
- data retention procedures

## Current Limitations

The current semantic response system is more controlled than an LLM-based chatbot, but it is still experimental.

The model currently uses semantic similarity and structured response selection. It does not yet include a fully trained and validated production-level classifier for final experimental deployment.

Current limitations may include:

- imperfect theme prediction
- limited response diversity
- manually designed response categories
- possible notebook errors or unfinished analysis
- limited external testing

The notebook `semantic_pipeline_v1.ipynb` reflects exploratory work and may contain mistakes or unfinished sections.

## Future Work

Possible next steps include:

- reviewing response categories with the research team
- refining theme anchors and response banks
- testing the bot with mock participants
- improving CSV logging format
- generating example output datasets for collaborators
- preparing final IRB language
- deploying the bot to a server so it can run continuously without a local laptop
- improving interpretability metrics
- potentially integrating supervised classifiers such as Random Forest models trained on larger structured datasets
- finalizing handoff documentation for future developers or research assistants

## Suggested Immediate Priorities

For short-term project readiness:

1. Ensure all repository documentation is complete
2. Generate example participant datasets
3. Prepare presentation slides
4. Organize IRB drafts and reference papers into shared folders
5. Review code comments for clarity
6. Confirm reproducible local setup
7. Meet with handoff personnel for technical walkthrough

## Final Note

This repository represents a functional but evolving human-AI experimental platform.

The current Telegram bot and semantic response architecture provide a strong technical foundation, but final research deployment should prioritize:

- clarity
- reproducibility
- interpretability
- ethical compliance
- maintainability

Future contributors should treat this repository as both a technical tool and a research infrastructure project.
