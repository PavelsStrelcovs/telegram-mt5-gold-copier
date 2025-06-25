# Telegram to MT5 Gold Copier

This project is a Python bot that listens for GOLD trading signals in a Telegram channel and automatically places trades on MetaTrader 5 (MT5) using the MetaTrader5 Python API.

## Features
- Monitors a Telegram channel for GOLD (XAUUSD) trade signals in the format:
  ```
  GOLD BUY  - 3332
  TP - 3340
  SL - 3328
  ```
- Parses the signal and sends a market order to MT5 with entry, stop loss, and take profit.
- Logs all actions and errors for easy debugging.

## Requirements
- Python 3.7+
- [MetaTrader 5](https://www.metatrader5.com/) installed and logged in
- Telegram bot token ([create one with BotFather](https://core.telegram.org/bots#botfather))
- `MetaTrader5` and `python-telegram-bot` Python packages

## Setup
1. **Clone this repository:**
   ```bash
   git clone https://github.com/PavelsStrelcovs/telegram-mt5-gold-copier.git
   cd telegram-mt5-gold-copier
   ```
2. **Install dependencies:**
   ```bash
   pip install MetaTrader5 python-telegram-bot
   ```
3. **Edit `TGTOMT5.py`:**
   - Fill in your `BOT_TOKEN`, `MT5_LOGIN`, `MT5_PASSWORD`, `MT5_SERVER`, and `MT5_PATH`.
   - Make sure your bot is an admin in the Telegram channel.
   - Make sure MT5 is running and logged in.

## Usage
1. Run the script:
   ```bash
   python TGTOMT5.py
   ```
2. Send a GOLD signal in your Telegram channel in the format:
   ```
   GOLD BUY  - 3332
   TP - 3340
   SL - 3328
   ```
3. The bot will parse the message and place a trade on MT5.

## Security & Disclaimer
- **Never share your credentials publicly.**
- Use a demo account for testing.
- This script is for educational purposes. Use at your own risk.

---

Feel free to fork, modify, and contribute!
