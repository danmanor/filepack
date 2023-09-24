from pathlib import Path
import rarfile
from io import BytesIO
from types import TracebackType
from typing import Optional, Type

from archive.exceptions import (
    FailedToExtractArchiveFiles,
    FailedToGetArchiveMembers,
    FailedToAddNewMemberToArchive,
)
from archive.models import ArchiveMember, FileType, AbstractArchive


class RarArchive(AbstractArchive):
    def __init__(self, rar_file: rarfile.RarFile):
        self._rar_file = rar_file

    def __enter__(self) -> rarfile.RarFile:
        return self.__class__(rar_file=self._rar_file.__enter__())

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        self._rar_file.__exit__(typ=exc_type, value=exc_val, traceback=exc_tb)

    def extract_all(self, target_path: Optional[Path] = Path.cwd()):
        try:
            self._rar_file.extractall(path=target_path)

        except Exception as e:
            raise FailedToExtractArchiveFiles(
                f"failed to extract the rar archive members to {str(target_path)}"
            ) from e

    def get_members(self) -> list[ArchiveMember]:
        try:
            return [
                ArchiveMember(
                    name=rar_info.filename,
                    size=rar_info.file_size,
                    mtime=rar_info.date_time,
                    type=self._get_file_type(Path(rar_info.filename)),
                )
                for rar_info in self._rar_file.infolist()
            ]

        except Exception as e:
            raise FailedToGetArchiveMembers(
                "failed to extract the zip's members"
            ) from e

    def add(self, file_path: Path):
        raise FailedToAddNewMemberToArchive(
            "rar files does not support adding members"
        )

    def get_file_name_without_suffix(self) -> str:
        return self._rar_file.filename.replace(".rar", "")

    def add_file(
        self, zip_info: rarfile.RarInfo, file_object_content: Optional[BytesIO] = None
    ):
        raise FailedToAddNewMemberToArchive(
            "rar files does not support adding members"
        )

    @staticmethod
    def _get_file_type(file_path: Path) -> FileType:
        if file_path.is_dir():
            return FileType("directory")
        if file_path.is_file():
            return FileType("regular")
