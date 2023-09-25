from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Optional, Tuple

import filetype
import pytz


def reraise_as(exception_class=Exception):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise exception_class(
                    f"an error occurred: {str(e)}"
                ) from e

        return wrapper

    return decorator


def format_date_tuple(
    date_tuple: Tuple[int, int, int, int, int, int]
) -> str:
    israel_tz = pytz.timezone("Asia/Jerusalem")
    localized_dt = israel_tz.localize(datetime(*date_tuple))

    return localized_dt.astimezone(tz=timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S %Z"
    )


def get_file_type_extension(path: Path) -> Optional[str]:
    if (file_type := filetype.guess(path)) is None:
        raise ValueError("given file type is not recognized")
    return file_type.extension
