from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional, Type

import filetype
import pytz

from filepack.exceptions import OperationNotSupported


def reraise_as(
    exception_class: Type[Exception] = Exception,
) -> Callable[..., Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise exception_class(f"an error occurred: {str(e)}") from e

        return wrapper

    return decorator


def ensure_instance(
    attribute: str,
) -> Callable[..., Callable[..., Any]]:
    def ensure_instance(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            instance = getattr(self, attribute, None)
            if instance is None:
                raise OperationNotSupported()
            return func(self, *args, **kwargs)

        return wrapper

    return ensure_instance


def format_date_tuple(date_tuple: tuple[int, int, int, int, int, int]) -> str:
    israel_tz = pytz.timezone("Asia/Jerusalem")
    localized_dt = israel_tz.localize(datetime(*date_tuple))

    return localized_dt.astimezone(tz=timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S %Z"
    )


def get_file_type_extension(path: Path) -> Optional[str]:
    if (file_type := filetype.guess(path)) is None:
        raise ValueError("given file type is not recognized")
    return file_type.extension
