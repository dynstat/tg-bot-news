import threading
from tg_const import *
import logging

logging.basicConfig(
    level=logging.INFO,
)
from tgbot_all_funcs import updater, sender


if __name__ == "__main__":
    threading.Thread(target=updater, name="UPDATER").start()
    threading.Thread(target=sender, name="SENDER").start()
