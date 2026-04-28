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
