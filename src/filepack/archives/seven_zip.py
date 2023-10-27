import tempfile
from pathlib import Path
from typing import Optional

import py7zr

from filepack.archives.exceptions import ArchiveMemberDoesNotExist
from filepack.archives.models import (
    AbstractArchive,
    ArchiveMember,
    UnknownFileType,
)
from filepack.utils import get_file_type_extension


class SevenZipArchive(AbstractArchive):
    def __init__(
        self,
        path: Path,
    ):
        self._path = path

    def extract_member(self, member_name: str, target_path: str | Path):
        if not self.member_exist(member_name=member_name):
            raise ArchiveMemberDoesNotExist()

        with py7zr.SevenZipFile(file=self._path, mode="r") as seven_zip_file:
            seven_zip_file.extract(targets=[member_name], path=target_path)

    def get_member(self, member_name: str) -> Optional[ArchiveMember]:
        with py7zr.SevenZipFile(file=self._path, mode="r") as seven_zip_file:
            try:
                return self._seven_zip_info_to_archive_member(
                    [
                        member
                        for member in seven_zip_file.list()
                        if member.filename == member_name
                    ][0]
                )
            except IndexError:
                return None

    def get_members(self) -> list[ArchiveMember]:
        with py7zr.SevenZipFile(file=self._path, mode="r") as seven_zip_file:
            return [
                self._seven_zip_info_to_archive_member(
                    seven_zip_info=seven_zip_info
                )
                for seven_zip_info in seven_zip_file.list()
            ]

    def add_member(self, member_path: str | Path):
        member_path = Path(member_path)
        if not member_path.exists():
            raise FileNotFoundError()

        with py7zr.SevenZipFile(file=self._path, mode="a") as seven_zip_file:
            seven_zip_file.write(file=member_path, arcname=member_path.name)

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
            with py7zr.SevenZipFile(
                file=new_archive_path, mode="w"
            ) as new_file:
                for file in temporary_directory_members_path.iterdir():
                    new_file.write(file=file, arcname=file.name)

            new_archive_path.rename(self._path)

    def member_exist(self, member_name: str) -> bool:
        with py7zr.SevenZipFile(file=self._path, mode="r") as seven_zip_file:
            return member_name in [
                seven_zip_info.filename
                for seven_zip_info in seven_zip_file.list()
            ]

    def _get_seven_zip_info_file_type(
        self, seven_zip_info: py7zr.FileInfo
    ) -> str | UnknownFileType:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_file_path = (
                Path(temporary_directory) / seven_zip_info.filename
            )
            self.extract_member(
                member_name=seven_zip_info.filename,
                target_path=temporary_file_path,
            )

            try:
                type = get_file_type_extension(path=temporary_file_path)
                return type if type is not None else UnknownFileType()
            except Exception:
                return UnknownFileType()

    def _seven_zip_info_to_archive_member(
        self, seven_zip_info: py7zr.FileInfo
    ) -> ArchiveMember:
        return ArchiveMember(
            name=seven_zip_info.filename,
            size=seven_zip_info.compressed,
            mtime=seven_zip_info.creationtime,
            type=self._get_seven_zip_info_file_type(
                seven_zip_info=seven_zip_info
            ),
        )
