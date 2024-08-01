# My Initializer

import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from .clogging import getColoredLogger
from .path import get_current_dir, parent_search


def initializer(
    globals_: dict[str, object],
    logger: Optional[logging.Logger] = getColoredLogger(__name__),
    *,
    dotenv_filename: str = ".env",
) -> Path:
    """Initialize the environment
    Load the .env file and set the HUGGINGFACE_HUB_CACHE environment variable.

    Args:
        globals_ (dict[str, object]): The globals() dictionary.
        logger (Optional[logging.Logger], optional): The logger. Defaults to getColoredLogger(__name__).
        dotenv_filename (str, optional): The .env filename. Defaults to ".env".

    Returns:
        project_root_directory (Path): The detected project root directory.
        equal to __file__ (Python environment) or the current working directory (Jupyter environment).
    """
    logger.info("Initializing...")
    project_root_directory = Path(get_current_dir(globals_))
    DOTENV_PATH = parent_search(
        project_root_directory, dotenv_filename, enable_return_none=True
    )
    if DOTENV_PATH is None:
        logger.info("Could not detect .env file")
    else:
        logger.info(f"{DOTENV_PATH=}")
        load_dotenv(dotenv_path=project_root_directory.parent / dotenv_filename)

    HUGGINGFACE_HUB_CACHE = os.environ.get("HUGGINGFACE_HUB_CACHE", None)
    logger.info(f"{HUGGINGFACE_HUB_CACHE=}")

    CONTROL_SERVER_PREFIX = os.environ.get("CONTROL_SERVER_PREFIX", None)
    if CONTROL_SERVER_PREFIX is not None:
        logger.info(f"{CONTROL_SERVER_PREFIX=}")
        HOSTNAME = os.uname()[1]
        logger.info(f"{HOSTNAME=}")
        assert not HOSTNAME.startswith(
            CONTROL_SERVER_PREFIX
        ), f"{HOSTNAME=}, {CONTROL_SERVER_PREFIX=}"

    return project_root_directory
