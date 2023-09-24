from pathlib import Path
import zipfile
from io import BytesIO
from types import TracebackType
from typing import Optional, Type

from archive.exceptions import (
    FailedToExtractArchiveFiles,
    FailedToGetArchiveMembers,
    FailedToAddNewMemberToArchive,
)
from archive.models import ArchiveMember, FileType, AbstractArchive


class ZipArchive(AbstractArchive):
    def __init__(self, zip_file: zipfile.ZipFile):
        self._zip_file = zip_file

    def __enter__(self) -> zipfile.ZipFile:
        return self.__class__(zip_file=self._zip_file.__enter__())

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        self._zip_file.__exit__(type=exc_type, value=exc_val, traceback=exc_tb)

    def extract_all(self, target_path: Optional[Path] = Path.cwd()):
        try:
            self._zip_file.extractall(path=target_path)

        except Exception as e:
            raise FailedToExtractArchiveFiles(
                f"failed to extract the zip's members to {str(target_path)}"
            ) from e

    def get_members(self) -> list[ArchiveMember]:
        try:
            return [
                ArchiveMember(
                    name=zip_info.filename,
                    size=zip_info.file_size,
                    mtime=zip_info.date_time,
                    type=self._get_file_type(Path(zip_info.filename)),
                )
                for zip_info in self._zip_file.infolist()
            ]

        except Exception as e:
            raise FailedToGetArchiveMembers(
                "failed to extract the zip's members"
            ) from e

    def add(self, file_path: Path):
        try:
            self._zip_file.write(filename=file_path, arcname=file_path.name)

        except Exception as e:
            raise FailedToAddNewMemberToArchive(
                "failed to add new member to the zip archive"
            ) from e

    def get_file_name_without_suffix(self) -> str:
        return self._zip_file.filename.replace(".zip", "")

    def add_file(
        self, zip_info: zipfile.ZipInfo, file_object_content: Optional[BytesIO] = None
    ):
        try:
            self._zip_file.writestr(
                zinfo_or_arcname=zip_info,
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
