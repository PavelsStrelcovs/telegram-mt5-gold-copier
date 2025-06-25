import re
import logging
from telegram.ext import Application, MessageHandler, filters
import MetaTrader5 as mt5

# --- CONFIGURATION ---
BOT_TOKEN = '7905896669:AAGFW6U8kpkyUFXlujN4Jp5YV1dlnbyED5s'  # <-- Paste your bot token here
MT5_LOGIN = 52404529          # <-- Replace with your MT5 login
MT5_PASSWORD = '&00D@oX!tzfaKd'
MT5_SERVER = 'ICMarketsSC-Demo'
MT5_PATH = r'C:\Program Files\MetaTrader 5\terminal64.exe'
SYMBOL = 'XAUUSD'
LOT_SIZE = 0.01

logging.basicConfig(level=logging.INFO)

def parse_signal(text):
    text = text.upper()
    symbol_match = re.search(r'(GOLD|XAUUSD)\s+(BUY|SELL)\s*-\s*(\d+(\.\d+)?)', text)
    if symbol_match:
        signal = {
            'symbol': 'XAUUSD',
            'action': symbol_match.group(2),
            'entry': float(symbol_match.group(3))
        }
    else:
        return None

    tp_matches = re.findall(r'TP\s*[\d]*\s*-\s*(\d+(\.\d+)?)', text)
    signal['tp'] = [float(tp[0]) for tp in tp_matches]

    sl_match = re.search(r'SL\s*-\s*(\d+(\.\d+)?)', text)
    signal['sl'] = float(sl_match.group(1)) if sl_match else None

    return signal

def send_order(signal):
    logging.info(f"Attempting to send order: {signal}")
    if not mt5.initialize(path=MT5_PATH):
        logging.error("MT5 initialize() failed")
        return False
    if not mt5.login(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        logging.error("MT5 login() failed")
        return False

    symbol = signal['symbol']
    action = signal['action']
    price = signal['entry']
    sl = signal['sl']
    tp = signal['tp'][0] if signal['tp'] else None
    lot = LOT_SIZE

    order_type = mt5.ORDER_TYPE_BUY if action == 'BUY' else mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "Telegram Bot Signal",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    if sl:
        request["sl"] = sl
    if tp:
        request["tp"] = tp

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.error(f"Trade failed: {result.retcode} - {result.comment}")
        return False
    logging.info(f"Trade executed: Order #{result.order} - {symbol} {action} {lot} lots")
    mt5.shutdown()
    return True

async def handle_message(update, context):
    logging.info(f"Update received: {update}")
    msg = update.message if update.message else update.channel_post
    if not msg or not msg.text:
        logging.info("Ignored non-text message or empty message.")
        return
    text = msg.text
    logging.info(f"Received message: {text}")
    signal = parse_signal(text)
    if signal:
        logging.info(f"Parsed signal: {signal}")
        success = send_order(signal)
        if success:
            logging.info("Trade sent to MT5 successfully.")
        else:
            logging.error("Failed to send trade to MT5.")
    else:
        logging.info("No valid GOLD signal found in message.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
