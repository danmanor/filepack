from pathlib import Path
import tarfile
from io import BytesIO
from types import TracebackType
from typing import Optional, Type

from archive.exceptions import (
    FailedToExtractArchiveFiles,
    FailedToGetArchiveMembers,
    FailedToAddNewMemberToArchive,
)
from archive.models import ArchiveMember, FileType, AbstractArchive


class TarArchive(AbstractArchive):
    def __init__(self, tar_file: tarfile.TarFile):
        self._tar_file = tar_file

    def __enter__(self) -> tarfile.TarFile:
        return self.__class__(tar_file=self._tar_file.__enter__())

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        self._tar_file.__exit__(type=exc_type, value=exc_val, traceback=exc_tb)

    def extract_all(self, target_path: Optional[Path] = Path.cwd()):
        try:
            self._tar_file.extractall(target_path)

        except Exception as e:
            raise FailedToExtractArchiveFiles(
                f"failed to extract the tar's content to {str(target_path)}"
            ) from e

    def get_members(self) -> list[ArchiveMember]:
        try:
            return [
                ArchiveMember(
                    name=tar_info.name,
                    size=tar_info.size,
                    mtime=tar_info.mtime,
                    type=self._convert_tar_info_type_to_file_type(tar_info.type),
                )
                for tar_info in self._tar_file.getmembers()
            ]

        except Exception as e:
            raise FailedToGetArchiveMembers(
                "failed to extract the tar's members"
            ) from e

    def add(self, file_path: Path):
        try:
            self._tar_file.add(name=file_path)

        except Exception as e:
            raise FailedToAddNewMemberToArchive(
                "failed to add new member to the tar"
            ) from e

    def get_file_name_without_suffix(self) -> str:
        return (
            self._tar_file.name.replace(".tar", "")
            .replace(".gz", "")
            .replace(".bz2", "")
        )

    def add_file(
        self, tar_info: tarfile.TarInfo, file_object_content: Optional[BytesIO] = None
    ):
        try:
            self._tar_file.addfile(tarinfo=tar_info, fileobj=file_object_content)

        except Exception as e:
            raise FailedToAddNewMemberToArchive(
                "failed to add new member to the tar archive"
            ) from e

    @staticmethod
    def _convert_tar_info_type_to_file_type(file_type: bytes) -> FileType:
        """REGTYPE = b"0"
        DIRTYPE = b"5"
        """

        match file_type:
            case b"0":
                return FileType("regular")
            case b"5":
                return FileType("directory")
            case _:
                return FileType("unsupported")
