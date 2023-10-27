from pathlib import Path
from typing import final

from filepack.compressions.bzip2 import BzipCompression
from filepack.compressions.exceptions import (
    FailedToCompressFile,
    FailedToDecompressFile,
    FailedToGetCompressedSize,
    FailedToGetUncompressedSize,
)
from filepack.compressions.gzip import GzipCompression
from filepack.compressions.lz4 import LZ4Compression
from filepack.compressions.models import AbstractCompression, CompressionType
from filepack.compressions.xz import XZCompression
from filepack.consts import ERROR_MESSAGE_NOT_SUPPORTED
from filepack.utils import get_file_type_extension, reraise_as


@final
class Compression:
    def __init__(self, path: Path) -> None:
        self._path = path

        self._path = Path(path)

        if not self._path.exists():
            try:
                self._type = CompressionType(self._path.suffix.lstrip("."))
            except Exception:
                raise ValueError(ERROR_MESSAGE_NOT_SUPPORTED)

        else:
            self._type = CompressionType(
                get_file_type_extension(path=self._path)
            )

        self._instance: AbstractCompression

        match self._type:
            case CompressionType.GZIP:
                self._instance = GzipCompression(
                    path=path,
                )

            case CompressionType.BZ2:
                self._instance = BzipCompression(
                    path=path,
                )

            case CompressionType.LZ4:
                self._instance = LZ4Compression(
                    path=path,
                )

            case CompressionType.XZ:
                self._instance = XZCompression(
                    path=path,
                )

    @property
    def path(self) -> Path:
        return self._path

    @property
    def suffix(self) -> str:
        return self._type.value

    @property
    @reraise_as(FailedToGetUncompressedSize)
    def uncompressed_size(self) -> int:
        return self._instance.uncompressed_size

    @property
    @reraise_as(FailedToGetCompressedSize)
    def compressed_size(self) -> int:
        return self._instance.compressed_size

    @property
    def compression_ratio(self) -> str:
        return self._instance.compression_ratio

    @reraise_as(FailedToDecompressFile)
    def decompress(self, target_path: str | Path):
        self._instance.decompress(target_path=target_path)

    @reraise_as(FailedToCompressFile)
    def compress(
        self,
        target_path: Path = Path.cwd(),
        compression_level: int = 9,
    ):
        self._instance.compress(
            target_path=target_path,
            compression_level=compression_level,
        )

    def is_compressed(self) -> bool:
        return self._instance.is_compressed()
