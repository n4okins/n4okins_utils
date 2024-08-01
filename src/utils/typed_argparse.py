import argparse
from collections.abc import Iterable
from dataclasses import _MISSING_TYPE, Field, asdict, dataclass, field
from typing import Any, Callable, Iterator, Literal, Optional

__all__ = ["TypedArgumentParser"]


@dataclass
class TypedArgument:
    name_or_flags: str | list[str]
    action: Literal[
        "store",
        "store_true",
        "store_false",
        "append",
        "append_const",
        "count",
        "help",
        "version",
    ] = "store"
    nargs: Optional[int | Literal["?", "*", "+"]] = None
    const: Any = None
    default: Any | Iterable[Any] = None
    type: type = str
    choices: Optional[list] = None
    required: Optional[bool] = None
    help: Optional[str] = None
    metavar: Optional[str | tuple[str, ...]] = None
    version: Optional[str] = None
    dest: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.name_or_flags, str):
            self.name_or_flags = [self.name_or_flags]

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


def targ(
    name_or_flags: str | list[str],
    action: Literal[
        "store",
        "store_true",
        "store_false",
        "append",
        "append_const",
        "count",
        "help",
        "version",
    ] = "store",
    nargs: Optional[int | Literal["?", "*", "+"]] = None,
    const: Any = None,
    default: Any | Iterable[Any] = None,
    type: object = str,
    choices: Optional[list] = None,
    required: Optional[bool] = None,
    help: Optional[str] = None,
    metavar: Optional[str | tuple[str, ...]] = None,
    version: Optional[str] = None,
    dest: Optional[str] = None,
) -> Field:
    metadata = {
        "name_or_flags": name_or_flags,
        "action": action,
        "nargs": nargs,
        "const": const,
        "type": type,
        "choices": choices,
        "required": required,
        "help": help,
        "metavar": metavar,
        "version": version,
        "dest": dest,
    }
    if isinstance(default, (list, tuple, set)):
        return field(default_factory=lambda: default, metadata=metadata)
    else:
        return field(default=default, metadata=metadata)


def typed_argument_class(cls: object) -> object:
    def wrapper(cls: object) -> object:
        items: dict[str, Field] = getattr(cls, "__dataclass_fields__", None)
        if items is None:
            d = dict(cls.__dict__)
            for k, t in cls.__annotations__.items():
                v = getattr(cls, k, _MISSING_TYPE())
                if isinstance(v, Field):
                    d[k] = v
                else:
                    d[k] = targ(name_or_flags=k, type=t, default=v)

            cls = type(cls.__name__, cls.__bases__, d)
            cls = dataclass(cls)
            items = getattr(cls, "__dataclass_fields__")

        def parse_args(cls: object) -> object:
            parser = argparse.ArgumentParser()
            for key, value in items.items():
                if not isinstance(value.default, _MISSING_TYPE) and isinstance(
                    value.default_factory, _MISSING_TYPE
                ):
                    data = dict(value.metadata)
                    data["default"] = value.default
                    kwargs = TypedArgument(**data)
                elif isinstance(value.default, _MISSING_TYPE) and not isinstance(
                    value.default_factory, _MISSING_TYPE
                ):
                    data = dict(value.metadata)
                    data["default"] = value.default_factory()
                    kwargs = TypedArgument(**data)
                else:
                    kwargs = TypedArgument(name_or_flags=[key], type=value.type)

                if kwargs.default is not None:
                    if isinstance(kwargs.default, (list, tuple, set)):
                        is_type_origin = isinstance(
                            kwargs.default, kwargs.type.__origin__
                        )
                        is_type_args = all(
                            isinstance(v, kwargs.type.__args__) for v in kwargs.default
                        )
                    elif not isinstance(kwargs.default, kwargs.type):
                        raise TypeError(
                            f"Type mismatch: {key} annotated as {kwargs.type} but {kwargs.default} is {type(kwargs.default)}"
                        )

                options = kwargs.to_dict()
                del options["name_or_flags"]
                parser.add_argument(*kwargs.name_or_flags, **options)
            return parser.parse_args()

        cls.parse_args = classmethod(parse_args)
        return cls

    return wrapper(cls)
