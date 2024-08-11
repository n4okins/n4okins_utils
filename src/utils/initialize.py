# My Initializer

import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from .clogging import getColoredLogger
from .git import is_in_gitignore
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
    PROJECT_ROOT_DIR = Path(get_current_dir(globals_))
    DOTENV_PATH = parent_search(
        PROJECT_ROOT_DIR, dotenv_filename, enable_return_none=True
    )
    GITIGNORE_PATH = parent_search(
        PROJECT_ROOT_DIR, ".gitignore", enable_return_none=True
    )
    if GITIGNORE_PATH is None:
        logger.info("Could not detect .gitignore file")
    else:
        logger.info(f"{GITIGNORE_PATH=}")

    if DOTENV_PATH is None:
        logger.info("Could not detect .env file")
    else:
        logger.info(f"{DOTENV_PATH=}")
        load_dotenv(dotenv_path=PROJECT_ROOT_DIR.parent / dotenv_filename)
        if GITIGNORE_PATH is not None and not is_in_gitignore(
            GITIGNORE_PATH, dotenv_filename
        ):
            logger.warning(
                f"dotenv file is detected at {DOTENV_PATH}, but `{dotenv_filename}` not in .gitignore (in {GITIGNORE_PATH})."
            )

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

    return PROJECT_ROOT_DIR
