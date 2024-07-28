import logging

from .colors import ColorCode, ColoredStr, JapaneseColorCode

__all__ = ["getColoredLogger"]


class ColoredStreamHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord): ...
