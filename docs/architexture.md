# Architecture

## Overview

This project is a Telegram Text-to-Speech bot developed with Python.

## Project Structure

core/
├── main.py        # Main bot logic
├── t.py           # Helper functions

voices/
voices2/
docs/

README.md
requirements.txt

## Workflow

1. User sends a message.
2. User selects a language.
3. The bot converts the text to speech.
4. The generated MP3 file is sent back.
5. Temporary audio files are removed.

## Technologies

- Python
- pyTelegramBotAPI
- gTTS
- Edge-TTS