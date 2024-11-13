import inspect
import logging
from typing import Optional

from .colors import JapaneseColorCode, Color, ColoredStr

__all__ = ["ColoredFormatter", "getColoredLogger", "ColoredFileHandler"]


class ColoredFileHandler(logging.FileHandler):
    def __init__(
        self,
        filename: str,
        mode: str = "a",
        encoding: Optional[str] = None,
        delay: bool = False,
        colormap: Optional[dict[str, Color]] = None,
    ):
        super().__init__(filename, mode, encoding, delay)
        self.setFormatter(
            ColoredFormatter(
                "%(asctime)s [%(levelname)s] %(message)s %(name)s L%(lineno)d %(funcName)s %(filename)s ",
                datefmt="%Y-%m-%d_%H:%M:%S",
                colormap=colormap,
            )
        )

    def emit(self, record: logging.LogRecord) -> None:
        if isinstance(record.levelname, ColoredStr):
            record.levelname = record.levelname._inner_text
        if isinstance(record.msg, ColoredStr):
            record.msg = record.msg._inner_text
        super().emit(record)


class ColoredFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        colormap: Optional[dict[str, Color]] = None,
    ):
        super().__init__(fmt, datefmt)
        self._colormap = colormap or {
            "DEBUG": JapaneseColorCode.AO,
            "INFO": JapaneseColorCode.WAKATAKEIRO,
            "WARNING": JapaneseColorCode.KIKUCHINASHIIRO,
            "ERROR": JapaneseColorCode.HIIRO,
            "CRITICAL": JapaneseColorCode.KURENAI,
        }

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        nest_level = (
            len(
                [
                    frame
                    for frame in inspect.getouterframes(inspect.currentframe())
                    if record.pathname == frame.filename
                ]
            )
            - 1
        )
        if levelname in self._colormap:
            if levelname == "CRITICAL":
                record.levelname = ColoredStr(
                    f"{levelname:^9}", bg=self._colormap[levelname]
                )
            else:
                record.levelname = ColoredStr(
                    f"{levelname:^9}", fg=self._colormap[levelname]
                )
            record.msg = ColoredStr(
                nest_level * "    " + str(record.msg), fg=self._colormap[levelname]
            )
        return super().format(record)


def getColoredLogger(
    name: Optional[str] = None,
    *,
    handlers: Optional[logging.Handler | list[logging.Handler]] = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            ColoredFormatter(
                "%(asctime)s [%(levelname)s] %(message)s %(name)s L%(lineno)d %(funcName)s %(filename)s ",
                datefmt="%Y-%m-%d_%H:%M:%S",
            )
        )
        logger.addHandler(handler)

    if handlers:
        if not isinstance(handlers, list):
            handlers = [handlers]
        for handler in handlers:
            logger.addHandler(handler)

    logger.propagate = False
    return logger
