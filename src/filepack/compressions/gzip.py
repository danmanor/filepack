import gzip
from pathlib import Path
from typing import TextIO

from filepack.compressions.models import AbstractCompression


class GzipCompression(AbstractCompression):
    def __init__(self, path: Path) -> None:
        super().__init__(path=path)

    def _open(
        self,
        file_path: str | Path,
        mode: str = "r",
        compression_level=9,
    ) -> gzip.GzipFile | TextIO:
        return gzip.open(
            filename=file_path,
            mode=mode,
            compresslevel=compression_level,
        )
