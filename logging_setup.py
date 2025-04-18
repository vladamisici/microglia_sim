import logging
import sys

def setup_logging(level=logging.DEBUG, log_file=None):
    """
    Configure root logger: logs to console or file with DEBUG level by default.
    """
    fmt = '%(asctime)s %(name)s %(levelname)s: %(message)s'
    handlers = []
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    else:
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(level=level, format=fmt, handlers=handlers)
    