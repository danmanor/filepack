import os
import shutil
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

from filepack.compressions.consts import (
    BZ2_SUFFIX,
    GZIP_SUFFIX,
    LZ4_SUFFIX,
    XZ_SUFFIX,
)
from filepack.compressions.exceptions import (
    FileAlreadyCompressed,
    FileNotCompressed,
)
from filepack.utils import get_file_type_extension


class CompressionType(Enum):
    GZIP = GZIP_SUFFIX
    XZ = XZ_SUFFIX
    LZ4 = LZ4_SUFFIX
    BZ2 = BZ2_SUFFIX


class AbstractCompression(ABC):
    def __init__(self, path: Path) -> None:
        self._path = path
        self._suffix = path.suffix.lstrip(".")
        self._dot_suffix = path.suffix

    @property
    def uncompressed_size(self) -> int:
        if not self.is_compressed():
            return self._path.stat().st_size

        with self._open(file_path=self._path, mode="rb") as file:
            file.seek(0, os.SEEK_END)
            return file.tell()

    @property
    def compressed_size(self) -> int:
        if not self.is_compressed():
            raise FileNotCompressed()

        return self._path.stat().st_size

    @property
    def compression_ratio(self) -> str:
        ratio = round(
            self.uncompressed_size / self.compressed_size, 2
        )
        return f"{ratio}:1"

    @abstractmethod
    def _open(
        self,
        file_path: str | Path,
        mode: str = "r",
        compression_level=9,
    ):
        pass

    def decompress(self, target_path: str | Path):
        if not self.is_compressed():
            raise FileNotCompressed()

        with self._open(
            file_path=self._path, mode="rb"
        ) as compressed_file:
            with open(
                file=target_path, mode="wb"
            ) as decompressed_file:
                shutil.copyfileobj(
                    fsrc=compressed_file, fdst=decompressed_file
                )

    def compress(
        self,
        target_path: Path = Path.cwd(),
        compression_level: int = 9,
    ):
        if self.is_compressed():
            raise FileAlreadyCompressed()

        with open(file=self._path, mode="rb") as uncompressed_file:
            with self._open(
                file_path=target_path,
                mode="wb",
                compression_level=compression_level,
            ) as compressed_file:
                shutil.copyfileobj(
                    fsrc=uncompressed_file, fdst=compressed_file
                )

    def is_compressed(self) -> bool:
        try:
            return (
                get_file_type_extension(path=self._path)
                == self._suffix
            )
        except Exception:
            return False
