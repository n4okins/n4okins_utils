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


def is_in_gitignore(gitignore_path: Path, pattern: str) -> bool:
    """Check if the pattern is in the .gitignore file of the Git repository.
    Args:
        gitignore_path (Path): The .gitignore file.
        pattern (str): The pattern.
    Returns:
        bool: Whether the pattern is in the .gitignore file.
    """
    with open(gitignore_path, "r") as f:
        for line in f:
            if line.strip() == pattern:
                return True
    return False
