import html
import logging
import os
import requests


class TelegramHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        # otherwise error tags like '<>' cause issues
        log_entry_escaped = html.escape(log_entry)
        payload = {
            'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
            'text': log_entry_escaped,
            'parse_mode': 'HTML'
        }
        return requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_API_TOKEN')}/sendMessage",
                             data=payload).content


def get_logger(name='discoring-logger'):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        telegram_handler = TelegramHandler()
        telegram_handler.setLevel(logging.ERROR)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler.setFormatter(formatter)
        telegram_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(telegram_handler)

    return logger
