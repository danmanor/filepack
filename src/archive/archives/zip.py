import tempfile
import zipfile
from pathlib import Path

from archive.exceptions import (
    ArchiveMemberDoesNotExist,
    FailedToAddNewMemberToArchive,
    FailedToExtractArchiveMember,
    FailedToGetArchiveMembers,
    FailedToRemoveArchiveMember,
)
from archive.models import AbstractArchive, ArchiveMember
from archive.utils import format_date_tuple, reraise_as


class ZipArchive(AbstractArchive):
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
        with zipfile.ZipFile(file=self.path, mode="r") as zip_file:
            zip_file.extract(member=member_name, path=target_path)

    @reraise_as(FailedToGetArchiveMembers)
    def get_members(self) -> list[ArchiveMember]:
        with zipfile.ZipFile(file=self.path, mode="r") as zip_file:
            return [
                ArchiveMember(
                    name=zip_info.filename,
                    size=zip_info.file_size,
                    mtime=format_date_tuple(zip_info.date_time),
                )
                for zip_info in zip_file.infolist()
            ]

    @reraise_as(FailedToAddNewMemberToArchive)
    def add_member(self, member_path: str | Path):
        with zipfile.ZipFile(file=self.path, mode="a") as zip_file:
            zip_file.write(
                filename=member_path, arcname=Path(member_path).name
            )

    @reraise_as(FailedToRemoveArchiveMember)
    def remove_member(self, member_name: str):
        if self.get_member(member_name) is None:
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

            with zipfile.ZipFile(new_archive_path, "w") as new_file:
                for (
                    file
                ) in temporary_directory_members_path.iterdir():
                    new_file.write(filename=file, arcname=file.name)

            new_archive_path.rename(self.path)


"""     @staticmethod
    def _get_zip_info_content(zip_info: zipfile.ZipInfo) -> bytes:
        with open(zip_info.filename, "r") as file:
            return Path(file).read_bytes() """
