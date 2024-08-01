from pathlib import Path


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
