# My Initializer

import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from .clogging import getColoredLogger
from .git import get_git_root, is_in_gitignore
from .path import get_file_parent_dir, parent_search


def initializer(
    globals_: dict[str, object],
    *,
    dotenv_filename: str = ".env",
    logger: Optional[logging.Logger] = getColoredLogger(__name__),
) -> Path:
    """Initialize the environment
    Load the .env file and set the HUGGINGFACE_HUB_CACHE environment variable.

    Args:
        globals_ (dict[str, object]): The globals() dictionary.
        logger (Optional[logging.Logger], optional): The logger. Defaults to getColoredLogger(__name__).
        dotenv_filename (str, optional): The .env filename. Defaults to ".env".

    Returns:
        project_root_directory (Path): The detected project root directory.
        if .gitignore is detected, the project root directory is the directory containing the .git directory.
        if .env is detected, the project root directory is the parent directory of the .env file.
        Otherwise, the project root directory is the parent directory of the script.
    """
    logger.info("Initializing...")
    FILE_PARENT_DIR = Path(get_file_parent_dir(globals_))
    DOTENV_PATH = parent_search(
        FILE_PARENT_DIR, dotenv_filename, enable_return_none=True
    )
    GITIGNORE_PATH = parent_search(
        FILE_PARENT_DIR, ".gitignore", enable_return_none=True
    )
    if GITIGNORE_PATH is None:
        logger.warning("Could not detect .gitignore file")
    else:
        logger.info(f"{GITIGNORE_PATH=}")

    if DOTENV_PATH is None:
        logger.warning("Could not detect .env file")
    else:
        logger.info(f"{DOTENV_PATH=}")
        load_dotenv(dotenv_path=FILE_PARENT_DIR.parent / dotenv_filename)
        if GITIGNORE_PATH is not None and not is_in_gitignore(
            GITIGNORE_PATH, dotenv_filename
        ):
            logger.warning(
                f"dotenv file is detected at {DOTENV_PATH}, but `{dotenv_filename}` not in .gitignore (in {GITIGNORE_PATH})."
            )

    if GITIGNORE_PATH is not None:
        PROJECT_ROOT_DIR = get_git_root(FILE_PARENT_DIR)
    if PROJECT_ROOT_DIR is None and DOTENV_PATH is not None:
        PROJECT_ROOT_DIR = DOTENV_PATH.parent
    if PROJECT_ROOT_DIR is None:
        PROJECT_ROOT_DIR = FILE_PARENT_DIR

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
