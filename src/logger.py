from config import config
import gc

log_level = config['log_level']


def debug(message):
    if log_level in ['DEBUG']:
        print(message)


def info(message):
    if log_level in ['DEBUG', 'INFO']:
        print(message)


def error(message):
    if log_level in ['DEBUG', 'INFO', 'ERROR']:
        print(message)


def mem(message):
    if log_level in ['DEBUG', 'MEM']:
        print(message + ": ", gc.mem_free())
