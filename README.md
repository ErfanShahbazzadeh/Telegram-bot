# Python Telegram Bot with JSON Logging

This project is an asynchronous Telegram bot built with the `python-telegram-bot` library. It features an interactive menu system using inline buttons, basic conversational responses, and a persistence layer that saves user chat history to a local JSON file.

## 📖 About The Project

This bot demonstrates how to handle state and user data in a chat environment. Unlike simple "echo" bots, this project:
1.  **Tracks User History:** It creates a profile for every new user and logs their messages and the bot's responses into a JSON file.
2.  **Uses Inline Menus:** It implements a multi-page navigation system inside the chat using clickable buttons (Page 1, 2, 3).
3.  **Handles Logic:** It recognizes specific phrases (e.g., "Hello there" triggers "General Kenobi").

## 🛠️ Built With

* **Python 3.x**
* **python-telegram-bot** (v20+)
* **JSON** (Native Python library for data storage)

## ⚙️ Configuration & Setup

### 1. Prerequisites
You need to install the Telegram bot wrapper:
```sh
pip install python-telegram-bot
