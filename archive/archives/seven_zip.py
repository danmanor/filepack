from pathlib import Path
import py7zr
from io import BytesIO
from types import TracebackType
from typing import Optional, Type

from archive.exceptions import (
    FailedToExtractArchiveFiles,
    FailedToGetArchiveMembers,
    FailedToAddNewMemberToArchive,
)
from archive.models import ArchiveMember, FileType, AbstractArchive


class SevenZipArchive(AbstractArchive):
    def __init__(self, seven_zip_file: py7zr.SevenZipFile):
        self._seven_zip_file = seven_zip_file

    def __enter__(self) -> py7zr.SevenZipFile:
        return self.__class__(seven_zip_file=self._seven_zip_file.__enter__())

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        self._seven_zip_file.__exit__(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)

    def extract_all(self, target_path: Optional[Path] = Path.cwd()):
        try:
            self._seven_zip_file.extractall(path=target_path)

        except Exception as e:
            raise FailedToExtractArchiveFiles(
                f"failed to extract the seven zip archive members to {str(target_path)}"
            ) from e

    def get_members(self) -> list[ArchiveMember]:
        try:
            return [
                ArchiveMember(
                    name=seven_zip_info.filename,
                    size=seven_zip_info.compressed,
                    mtime=seven_zip_info.creationtime,
                    type=self._get_file_type(Path(seven_zip_info.filename)),
                )
                for seven_zip_info in self._seven_zip_file.list()
            ]

        except Exception as e:
            raise FailedToGetArchiveMembers(
                "failed to extract the zip's members"
            ) from e

    def add(self, file_path: Path):
        try:
            self._seven_zip_file.write(file=file_path, arcname=file_path.name)

        except Exception as e:
            raise FailedToAddNewMemberToArchive(
                "failed to add new member to the 7zip archive"
            ) from e

    def get_file_name_without_suffix(self) -> str:
        return self._seven_zip_file.filename.replace(".7z", "")

    def add_file(
        self, seven_zip_info: py7zr.FileInfo, file_object_content: Optional[BytesIO] = None
    ):
        try:
            self._seven_zip_file.writestr(
                arcname=seven_zip_info.filename,
                data=file_object_content
            )

        except Exception as e:
            raise FailedToAddNewMemberToArchive(
                "failed to add new member to the zip archive"
            ) from e

    @staticmethod
    def _get_file_type(file_path: Path) -> FileType:
        if file_path.is_dir():
            return FileType("directory")
        if file_path.is_file():
            return FileType("regular")
