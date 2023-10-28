import os
import shutil
import tempfile
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
    def __init__(self, path: Path, extension: str) -> None:
        self._path = path
        self._suffix = path.suffix.lstrip(".")
        self._dot_suffix = path.suffix
        self._extension = extension

    def uncompressed_size(self) -> int:
        if not self.is_compressed():
            return self._path.stat().st_size

        with tempfile.NamedTemporaryFile() as temporary_file:
            self.decompress(target_path=temporary_file.name)
            return Path(temporary_file.name).stat().st_size

    def compressed_size(self, compression_level: int | None = None) -> int:
        if not self.is_compressed():
            if compression_level is None:
                raise ValueError(
                    (
                        "Failed to infer the compressed size"
                        "of an uncompressed file"
                        "- need compression level"
                    )
                )
            with tempfile.NamedTemporaryFile() as temporary_file:
                self.compress(
                    target_path=temporary_file.name,
                    compression_level=compression_level,
                )
                return Path(temporary_file.name).stat().st_size

        return self._path.stat().st_size

    def compression_ratio(self) -> str:
        ratio = round(self.uncompressed_size() / self.compressed_size(), 2)
        return f"{ratio}:1"

    @abstractmethod
    def _open(
        self,
        file_path: str | Path,
        mode: str = "rb",
        compression_level: int = 9,
    ):
        pass

    def compress(
        self,
        target_path: str | Path | None = None,
        compression_level: int = 9,
    ) -> Path:
        if self.is_compressed():
            raise FileAlreadyCompressed()

        switch_files_flag = False
        with tempfile.NamedTemporaryFile(delete=False) as temporary_file:
            with open(file=self._path, mode="rb") as uncompressed_file:
                if target_path is None:
                    target_path = temporary_file.name
                    switch_files_flag = True
                with self._open(
                    file_path=target_path,
                    mode="wb",
                    compression_level=compression_level,
                ) as compressed_file:
                    shutil.copyfileobj(
                        fsrc=uncompressed_file, fdst=compressed_file
                    )

            if switch_files_flag:
                os.remove(self._path)
                self._path = Path(str(self._path) + "." + self._extension)
                os.rename(src=temporary_file.name, dst=self._path)

        return self._path

    def decompress(self, target_path: str | Path | None = None) -> Path:
        if not self.is_compressed():
            raise FileNotCompressed()

        switch_files_flag = False
        with tempfile.NamedTemporaryFile(delete=False) as temporary_file:
            with self._open(
                file_path=self._path, mode="rb"
            ) as compressed_file:
                if target_path is None:
                    target_path = temporary_file.name
                    switch_files_flag = True
                with open(file=target_path, mode="wb") as decompressed_file:
                    shutil.copyfileobj(
                        fsrc=compressed_file, fdst=decompressed_file
                    )

            if switch_files_flag:
                os.remove(self._path)
                self._path = Path(self._path.parent / self._path.stem)
                os.rename(src=temporary_file.name, dst=self._path)

        return self._path

    def is_compressed(self) -> bool:
        try:
            return get_file_type_extension(self._path) == self._extension
        except ValueError:
            return False
