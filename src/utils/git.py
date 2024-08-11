from pathlib import Path

from .path import parent_search


def get_git_root(path: Path) -> Path:
    """Get the root directory of the Git repository.
    Args:
        path (Path): The starting directory.
    Returns:
    """
    return parent_search(path, ".git", enable_return_none=False).parent


def get_git_ignore(path: Path) -> Path:
    """Get the .gitignore file of the Git repository.
    Args:
        path (Path): The starting directory.
    Returns:
    """
    return parent_search(path, ".gitignore", enable_return_none=False)


def is_in_gitignore(path: Path, pattern: str) -> bool:
    """Check if the pattern is in the .gitignore file of the Git repository.
    Args:
        path (Path): The starting directory.
        pattern (str): The pattern.
    Returns:
        bool: Whether the pattern is in the .gitignore file.
    """
    git_ignore = get_git_ignore(get_git_root(path))
    with open(git_ignore, "r") as f:
        return pattern in f.read()
