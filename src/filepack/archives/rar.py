from pathlib import Path

import rarfile

from filepack.archives.exceptions import (
    ArchiveMemberDoesNotExist,
    FailedToAddNewMemberToArchive,
    FailedToRemoveArchiveMember,
)
from filepack.archives.models import (
    AbstractArchive,
    ArchiveMember,
    UnknownFileType,
)
from filepack.utils import format_date_tuple


class RarArchive(AbstractArchive):
    def __init__(
        self,
        path: Path,
    ):
        self._path = path

    def extract_member(
        self, member_name: str, target_path: str | Path
    ):
        if self.get_member(member_name=member_name) is None:
            raise ArchiveMemberDoesNotExist()

        with rarfile.RarFile(file=self._path, mode="r") as rar_file:
            rar_file.extract(member=member_name, path=target_path)

    def get_members(self) -> list[ArchiveMember]:
        with rarfile.RarFile(file=self._path, mode="r") as rar_file:
            return [
                ArchiveMember(
                    name=rar_info.filename,
                    size=rar_info.file_size,
                    mtime=format_date_tuple(rar_info.date_time),
                    type=UnknownFileType(),
                )
                for rar_info in rar_file.infolist()
            ]

    def add_member(self, member_path: str | Path):
        raise FailedToAddNewMemberToArchive(
            "rar files does not support adding members"
        )

    def remove_member(self, member_name: str):
        raise FailedToRemoveArchiveMember(
            "rar files does not support removing members"
        )
