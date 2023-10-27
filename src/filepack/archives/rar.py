import tempfile
from pathlib import Path
from typing import Optional

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
from filepack.utils import format_date_tuple, get_file_type_extension


class RarArchive(AbstractArchive):
    def __init__(
        self,
        path: Path,
    ):
        self._path = path

    def extract_member(self, member_name: str, target_path: str | Path):
        if not self.member_exist(member_name=member_name):
            raise ArchiveMemberDoesNotExist()

        with rarfile.RarFile(file=self._path, mode="r") as rar_file:
            rar_file.extract(member=member_name, path=target_path)

    def get_member(self, member_name: str) -> Optional[ArchiveMember]:
        with rarfile.RarFile(file=self._path, mode="r") as rar_file:
            try:
                return self._rar_info_to_archive_member(
                    rar_file.getinfo(name=member_name)
                )
            except rarfile.NoRarEntry:
                return None

    def get_members(self) -> list[ArchiveMember]:
        with rarfile.RarFile(file=self._path, mode="r") as rar_file:
            return [
                self._rar_info_to_archive_member(rar_info=rar_info)
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

    def member_exist(self, member_name: str) -> bool:
        with rarfile.RarFile(file=self._path, mode="r") as rar_file:
            return member_name in [
                rar_info.filename for rar_info in rar_file.infolist()
            ]

    def _get_rar_info_file_type(
        self, rar_info: rarfile.RarInfo
    ) -> str | UnknownFileType:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_file_path = Path(temporary_directory) / rar_info.filename
            self.extract_member(
                member_name=rar_info.filename,
                target_path=temporary_file_path,
            )

            try:
                type = get_file_type_extension(path=temporary_file_path)
                return type if type is not None else UnknownFileType()
            except Exception:
                return UnknownFileType()

    def _rar_info_to_archive_member(
        self, rar_info: rarfile.RarInfo
    ) -> ArchiveMember:
        return ArchiveMember(
            name=rar_info.filename,
            size=rar_info.file_size,
            mtime=format_date_tuple(rar_info.date_time),
            type=self._get_rar_info_file_type(rar_info=rar_info),
        )
