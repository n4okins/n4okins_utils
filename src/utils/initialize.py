# My Initializer

import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from .clogging import getColoredLogger
from .path import parent_search


def initializer(
    root: Path | str,
    logger: Optional[logging.Logger] = getColoredLogger(__name__),
    *,
    dotenv_filename: str = ".env",
) -> None:
    logger.info("Initializing...")
    root = Path(root)
    DOTENV_PATH = parent_search(root, dotenv_filename)
    logger.info(f"{DOTENV_PATH=}")
    load_dotenv(dotenv_path=root.parent / dotenv_filename)

    HUGGINGFACE_HUB_CACHE = os.environ.get("HUGGINGFACE_HUB_CACHE", None)
    logger.info(f"{HUGGINGFACE_HUB_CACHE=}")
    CONTROL_SERVER_PREFIX = os.environ.get("CONTROL_SERVER_PREFIX", None)
    logger.info(f"{CONTROL_SERVER_PREFIX=}")
    if CONTROL_SERVER_PREFIX is not None:
        HOSTNAME = os.uname()[1]
        logger.info(f"{HOSTNAME=}")
        assert not HOSTNAME.startswith(
            CONTROL_SERVER_PREFIX
        ), f"{HOSTNAME=}, {CONTROL_SERVER_PREFIX=}"
