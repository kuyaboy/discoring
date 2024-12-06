import os
import logging
import requests


class TelegramHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_API_TOKEN')}/sendMessage",
                             data=payload).content


logger = logging.getLogger('discoring-logger')
logger.setLevel(logging.DEBUG)
logger.propagate = False

if logger.hasHandlers():
    logger.handlers.clear()

telegram_handler = TelegramHandler()
telegram_handler.setLevel(logging.ERROR)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console_handler.setFormatter(formatter)
telegram_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(telegram_handler)
