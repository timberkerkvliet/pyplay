from __future__ import annotations

import logging


def pyplay_logger():
    logger = logging.getLogger('pyplay')
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter(f'[%(asctime)s] [pyplay] %(message)s')
    )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger.info
