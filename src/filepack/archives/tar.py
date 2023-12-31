import tarfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from filepack.archives.exceptions import ArchiveMemberDoesNotExist
from filepack.archives.models import (
    AbstractArchive,
    ArchiveMember,
    UnknownFileType,
)
from filepack.utils import get_file_type_extension


class TarArchive(AbstractArchive):
    def __init__(
        self,
        path: Path,
    ):
        self._path = path

    def extract_member(
        self,
        member_name: str,
        target_path: str | Path,
    ):
        if not self.member_exist(member_name=member_name):
            raise ArchiveMemberDoesNotExist()

        with tarfile.open(self._path, "r") as tar_file:
            tar_file.extract(member=member_name, path=target_path)

    def get_member(self, member_name: str) -> Optional[ArchiveMember]:
        with tarfile.open(name=self._path, mode="r") as tar_file:
            try:
                return self._tar_info_to_archive_member(
                    tar_file.getmember(name=member_name)
                )
            except KeyError:
                return None

    def get_members(self) -> list[ArchiveMember]:
        with tarfile.open(self._path, "r") as tar_file:
            return [
                self._tar_info_to_archive_member(tar_info=tar_info)
                for tar_info in tar_file.getmembers()
            ]

    def add_member(self, member_path: str | Path):
        member_path = Path(member_path)
        if not member_path.exists():
            raise FileNotFoundError()

        with tarfile.open(self._path, "a") as tar_file:
            tar_file.add(name=member_path, arcname=member_path.name)

    def remove_member(self, member_name: str):
        if not self.member_exist(member_name=member_name):
            raise ArchiveMemberDoesNotExist()

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_directory_members_path = (
                Path(temporary_directory) / "files"
            )
            temporary_directory_members_path.mkdir()

            for member in self.get_members():
                if not member.name == member_name:
                    self.extract_member(
                        member_name=member.name,
                        target_path=temporary_directory_members_path,
                    )

            new_archive_path = Path(temporary_directory) / "new_archive"

            with tarfile.open(new_archive_path, "w") as new_file:
                for file in temporary_directory_members_path.iterdir():
                    new_file.add(name=file, arcname=file.name)

            new_archive_path.rename(self._path)

    def member_exist(self, member_name: str) -> bool:
        with tarfile.open(self._path, "r") as tar_file:
            return member_name in [
                tar_info.name for tar_info in tar_file.getmembers()
            ]

    def _get_tar_info_file_type(
        self, tar_info: tarfile.TarInfo
    ) -> str | UnknownFileType:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_file_path = Path(temporary_directory) / tar_info.name
            self.extract_member(
                member_name=tar_info.name,
                target_path=temporary_file_path,
            )

            try:
                type = get_file_type_extension(path=temporary_file_path)
                return type if type is not None else UnknownFileType()
            except Exception:
                return UnknownFileType()

    def _tar_info_to_archive_member(
        self, tar_info: tarfile.TarInfo
    ) -> ArchiveMember:
        return ArchiveMember(
            name=tar_info.name,
            size=tar_info.size,
            mtime=datetime.utcfromtimestamp(tar_info.mtime).strftime(
                "%a, %d %b %Y %H:%M:%S UTC"
            ),
            type=self._get_tar_info_file_type(tar_info=tar_info),
        )
