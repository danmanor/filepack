import lzma
from pathlib import Path
from typing import TextIO

from filepack.compressions.models import AbstractCompression


class XZCompression(AbstractCompression):
    def __init__(self, path: Path) -> None:
        super().__init__(path=path)

    def _open(
        self,
        file_path: str | Path,
        mode: str = "r",
        compression_level=None,
    ) -> lzma.LZMAFile | TextIO:
        return lzma.open(
            filename=file_path, mode=mode, preset=compression_level
        )
