import tempfile
from pathlib import Path

import py7zr

from archive.exceptions import (
    ArchiveMemberDoesNotExist,
    FailedToAddNewMemberToArchive,
    FailedToExtractArchiveMember,
    FailedToGetArchiveMembers,
    FailedToRemoveArchiveMember,
)
from archive.models import AbstractArchive, ArchiveMember
from archive.utils import reraise_as


class SevenZipArchive(AbstractArchive):
    def __init__(
        self,
        path: Path,
    ):
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    @reraise_as(FailedToExtractArchiveMember)
    def extract_member(
        self, member_name: str, target_path: str | Path
    ):
        if self.get_member(member_name=member_name) is None:
            raise ArchiveMemberDoesNotExist()

        with py7zr.SevenZipFile(
            file=self.path, mode="r"
        ) as seven_zip_file:
            seven_zip_file.extract(
                targets=[member_name], path=target_path
            )

    @reraise_as(FailedToGetArchiveMembers)
    def get_members(self) -> list[ArchiveMember]:
        with py7zr.SevenZipFile(
            file=self.path, mode="r"
        ) as seven_zip_file:
            return [
                ArchiveMember(
                    name=seven_zip_info.filename,
                    size=seven_zip_info.compressed,
                    mtime=seven_zip_info.creationtime,
                )
                for seven_zip_info in seven_zip_file.list()
            ]

    @reraise_as(FailedToAddNewMemberToArchive)
    def add_member(self, member_path: Path):
        member_path = Path(member_path)
        if not member_path.exists():
            raise FileNotFoundError()

        with py7zr.SevenZipFile(
            file=self.path, mode="a"
        ) as seven_zip_file:
            seven_zip_file.write(
                file=member_path, arcname=member_path.name
            )

    @reraise_as(FailedToRemoveArchiveMember)
    def remove_member(self, member_name: str):

        if self.get_member(member_name=member_name) is None:
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

            new_archive_path = (
                Path(temporary_directory) / "new_archive"
            )
            with py7zr.SevenZipFile(
                file=new_archive_path, mode="w"
            ) as new_file:
                for (
                    file
                ) in temporary_directory_members_path.iterdir():
                    new_file.write(file=file, arcname=file.name)

            new_archive_path.rename(self.path)
