import os
import logging
import datetime
from pathlib import Path

def set_logger():
    logs_dir = os.path.join(Path(__file__).resolve().parent, "test_logs")

    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
    logfile = logs_dir + f"/TestDatabase_{current_time}.log"
    print(logfile)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Remove all handlers from the logger
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create a file handler
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.debug("Logger set up")