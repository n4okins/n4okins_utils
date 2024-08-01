from pathlib import Path


def parent_search(
    path: Path, name: str, enable_return_none: bool = True
) -> Path | None:
    """
    Search for a directory with the given name in the parent directories of the given path.
    Args:
        path (Path): The starting directory.
        name (str): The directory name to search for.
        enable_return_none (bool, optional): Whether to raise an error if the directory is not found. Defaults to True.

    Returns:
        Path: The directory with the given name.
        or None if the directory is not found and can_raise_error is False.
    """
    while True:
        if (path / name).exists():
            return path / name
        if path == path.parent and not enable_return_none:
            raise FileNotFoundError(
                f"Could not find {name} in the parent directories of {path}"
            )
        elif path == Path("/"):
            if not enable_return_none:
                raise FileNotFoundError(
                    f"Could not find {name} in the parent directories of {path}"
                )
            else:
                return None
        path = path.parent


def get_current_dir(_globals_dict: dict) -> Path:
    """Get the current directory of the Python script or Jupyter notebook.
    If the script is running in a Jupyter notebook, return the current working directory.
    Args:
        _globals_dict (dict): The globals() dictionary.
    Returns:
        Path object: The current directory.
    """
    _file_ = _globals_dict.get("__file__", None)
    return Path.cwd() if _file_ is None else Path(_file_).parent
