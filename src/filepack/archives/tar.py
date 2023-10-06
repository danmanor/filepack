import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

from filepack.archives.exceptions import ArchiveMemberDoesNotExist
from filepack.archives.models import AbstractArchive, ArchiveMember


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
        if self.get_member(member_name=member_name) is None:
            raise ArchiveMemberDoesNotExist()

        with tarfile.open(self._path, "r") as tar_file:
            tar_file.extract(member=member_name, path=target_path)

    def get_members(self) -> list[ArchiveMember]:
        with tarfile.open(self._path, "r") as tar_file:
            return [
                ArchiveMember(
                    name=tar_info.name,
                    size=tar_info.size,
                    mtime=datetime.utcfromtimestamp(
                        tar_info.mtime
                    ).strftime("%a, %d %b %Y %H:%M:%S UTC"),
                )
                for tar_info in tar_file.getmembers()
            ]

    def add_member(self, member_path: str | Path):
        member_path = Path(member_path)
        if not member_path.exists():
            raise FileNotFoundError()

        with tarfile.open(self._path, "a") as tar_file:
            tar_file.add(name=member_path, arcname=member_path.name)

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

            with tarfile.open(new_archive_path, "w") as new_file:
                for (
                    file
                ) in temporary_directory_members_path.iterdir():
                    new_file.add(name=file, arcname=file.name)

            new_archive_path.rename(self._path)
