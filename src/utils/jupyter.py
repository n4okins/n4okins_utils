def is_jupyter(_global: dict) -> bool:
    """Check if the code is running in a Jupyter notebook.

    Args:
        _global (dict, optional): The globals(). Defaults to globals().

    Returns:
        bool: True if running in Jupyter notebook, False otherwise.
    """
    if "get_ipython" not in _global:
        return False
    if _global["get_ipython"]().__class__.__name__ == "TerminalInteractiveShell":
        return False
    return True
