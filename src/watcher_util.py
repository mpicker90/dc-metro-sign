from config import config
from microcontroller import watchdog as w
from watchdog import WatchDogMode
import time
import logger

auto_restart = config['auto_restart']

def setup_watcher():
    if auto_restart:
        w_timeout = 15
        w.timeout = w_timeout
        w.mode = WatchDogMode.RESET
        w.feed()
    else:
        logger.info("Auto restart disabled")


def force_restart():
    try:
        w_timeout = 1
        w.timeout = w_timeout
        w.mode = WatchDogMode.RESET
    except Exception as e:
        logger.info("Watcher setup already")

    time.sleep(30)


def feed():
    if auto_restart:
        try:
            w.feed()
        except Exception as e:
            logger.info("Watcher not setup")
