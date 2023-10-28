from pathlib import Path
from typing import TextIO

import lz4.frame

from filepack.compressions.models import AbstractCompression, CompressionType


class LZ4Compression(AbstractCompression):
    def __init__(self, path: Path) -> None:
        super().__init__(path=path, extension=CompressionType.LZ4.value)

    def _open(
        self,
        file_path: str | Path,
        mode: str = "r",
        compression_level=9,
    ) -> lz4.frame.LZ4FrameFile | TextIO:
        return lz4.frame.open(
            filename=file_path,
            mode=mode,
            compression_level=compression_level,
        )
