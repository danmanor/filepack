import bz2
from pathlib import Path
from typing import TextIO

from filepack.compressions.models import AbstractCompression, CompressionType


class BzipCompression(AbstractCompression):
    def __init__(self, path: Path) -> None:
        super().__init__(path=path, extension=CompressionType.BZ2.value)

    def _open(
        self,
        file_path: str | Path,
        mode: str = "r",
        compression_level=9,
    ) -> bz2.BZ2File | TextIO:
        return bz2.open(
            filename=file_path,
            mode=mode,
            compresslevel=compression_level,
        )
