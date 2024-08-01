from pathlib import Path
from typing import Callable


def parent_search(path: Path, name: str) -> Path:
    """
    Search for a directory with the given name in the parent directories of the given path.
    """
    while True:
        if (path / name).exists():
            return path / name
        if path == path.parent:
            raise FileNotFoundError(
                f"Could not find {name} in the parent directories of {path}"
            )
        elif path == Path("/"):
            raise FileNotFoundError(
                f"Could not find {name} in the parent directories of {path}"
            )
        path = path.parent


def get_current_dir(_globals: Callable[[], dict]) -> Path:
    _file_ = _globals().get("__file__", None)
    return Path.cwd() if _file_ is None else Path(_file_).parent
