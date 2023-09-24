import tarfile
import gzip
import zipfile
import rarfile
import py7zr

from pathlib import Path
from types import TracebackType
from typing import Optional, Type
from io import BytesIO

from archive.archives.tar import TarArchive
from archive.archives.seven_zip import SevenZipArchive
from archive.archives.zip import ZipArchive
from archive.archives.rar import RarArchive
from archive.models import AbstractArchive, ArchiveType, ArchiveMember


def open(path: Optional[Path], file_object: Optional[BytesIO] = None, mode: str = "r"):
    path = Path(path)
    try:
        type = ArchiveType(path.suffix)

    except Exception:
        raise ValueError("the given archive type is not supported")

    if type == ArchiveType.TAR:
        return Archive(
            instance=TarArchive(
                tar_file=tarfile.open(name=path, fileobj=file_object, mode=mode)
            ),
            type=type,
        )
    
    if type == ArchiveType.ZIP:
        file = path if path is not None else file_object
        return Archive(
            instance=ZipArchive(zip_file=zipfile.ZipFile(file=file, mode=mode)),
            type=type,
        )
    
    if type == ArchiveType.RAR:
        file = path if path is not None else file_object
        return Archive(
            instance=RarArchive(rar_file=rarfile.RarFile(file=file, mode=mode)),
            type=type,
        )
    
    if type == ArchiveType.SEVEN_ZIP:
        filename = path if path is not None else file_object
        return Archive(
            instance=SevenZipArchive(seven_zip_file=py7zr.SevenZipFile(file=filename, mode=mode)),
            type=type,
        )


class Archive:
    def __init__(self, instance: AbstractArchive, type: ArchiveType) -> None:
        self._instance = instance
        self._type = type

    def __enter__(self) -> AbstractArchive:
        return self._instance.__enter__()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        self._instance.__exit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)

    def extract_all(self, target_path: Path):
        self._instance.extract_all(target_path=target_path)

    def get_members(self) -> list[ArchiveMember]:
        return self._instance.get_members()

    def add(self, file_path: Path):
        self._instance.add(file_path=file_path)
