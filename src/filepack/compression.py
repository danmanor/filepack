from pathlib import Path
from typing import final

from filepack.compressions.bzip2 import BzipCompression
from filepack.compressions.exceptions import (
    CompressionTypeNotSupported,
    FailedToCompressFile,
    FailedToDecompressFile,
    FailedToGetCompressedSize,
    FailedToGetUncompressedSize,
)
from filepack.compressions.gzip import GzipCompression
from filepack.compressions.lz4 import LZ4Compression
from filepack.compressions.models import AbstractCompression, CompressionType
from filepack.compressions.xz import XZCompression
from filepack.utils import reraise_as


@final
class Compression:
    def __init__(self, path: Path) -> None:
        self._path = Path(path)

        if not self._path.exists():
            raise FileNotFoundError()

    @property
    def path(self) -> Path:
        return self._path

    @property
    def suffix(self) -> str:
        return self.path.suffix.lstrip(".")

    @reraise_as(FailedToGetUncompressedSize)
    def uncompressed_size(self, compression_algorithm: str) -> int:
        compression_instance = self._get_compression_instance(
            compression_algorithm=compression_algorithm
        )
        return compression_instance.uncompressed_size()

    @reraise_as(FailedToGetCompressedSize)
    def compressed_size(
        self, compression_algorithm: str, compression_level: int | None = None
    ) -> int:
        compression_instance = self._get_compression_instance(
            compression_algorithm=compression_algorithm,
        )
        return compression_instance.compressed_size(
            compression_level=compression_level
        )

    def compression_ratio(self, compression_algorithm: str) -> str:
        compression_instance = self._get_compression_instance(
            compression_algorithm=compression_algorithm
        )
        return compression_instance.compression_ratio()

    @reraise_as(FailedToDecompressFile)
    def decompress(
        self, compression_algorithm: str, target_path: str | Path | None = None
    ) -> Path:
        compression_instance = self._get_compression_instance(
            compression_algorithm=compression_algorithm
        )
        self._path = compression_instance.decompress(target_path=target_path)
        return self._path

    @reraise_as(FailedToCompressFile)
    def compress(
        self,
        compression_algorithm: str,
        target_path: str | Path | None = None,
        compression_level: int = 9,
    ) -> Path:
        compression_instance = self._get_compression_instance(
            compression_algorithm=compression_algorithm
        )
        self._path = compression_instance.compress(
            target_path=target_path,
            compression_level=compression_level,
        )
        return self._path

    def is_compressed(self, compression_algorithm: str) -> bool:
        compression_instance = self._get_compression_instance(
            compression_algorithm=compression_algorithm
        )
        return compression_instance.is_compressed()

    def _get_compression_instance(
        self, compression_algorithm: str
    ) -> AbstractCompression:
        try:
            match CompressionType(compression_algorithm):
                case CompressionType.GZIP:
                    return GzipCompression(
                        path=self.path,
                    )

                case CompressionType.BZ2:
                    return BzipCompression(
                        path=self.path,
                    )

                case CompressionType.LZ4:
                    return LZ4Compression(
                        path=self.path,
                    )

                case CompressionType.XZ:
                    return XZCompression(
                        path=self.path,
                    )
                case _:
                    raise CompressionTypeNotSupported()
        except Exception:
            raise CompressionTypeNotSupported()
