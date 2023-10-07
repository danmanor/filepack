import tempfile
import zipfile
from pathlib import Path

from filepack.archives.exceptions import ArchiveMemberDoesNotExist
from filepack.archives.models import (
    AbstractArchive,
    ArchiveMember,
    UnknownFileType,
)
from filepack.utils import format_date_tuple, get_file_type_extension


class ZipArchive(AbstractArchive):
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

        with zipfile.ZipFile(file=self._path, mode="r") as zip_file:
            zip_file.extract(member=member_name, path=target_path)

    def get_members(self) -> list[ArchiveMember]:
        with zipfile.ZipFile(file=self._path, mode="r") as zip_file:
            return [
                ArchiveMember(
                    name=zip_info.filename,
                    size=zip_info.file_size,
                    mtime=format_date_tuple(zip_info.date_time),
                    type=self._get_zip_info_file_type(
                        zip_info=zip_info
                    ),
                )
                for zip_info in zip_file.infolist()
            ]

    def add_member(self, member_path: str | Path):
        member_path = Path(member_path)
        if not member_path.exists():
            raise FileNotFoundError()

        with zipfile.ZipFile(file=self._path, mode="a") as zip_file:
            zip_file.write(
                filename=member_path, arcname=Path(member_path).name
            )

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

            new_archive_path.rename(self._path)

    def _get_zip_info_file_type(
        self, zip_info: zipfile.ZipInfo
    ) -> str | UnknownFileType:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_file_path = (
                Path(temporary_directory) / zip_info.filename
            )
            self.extract_member(
                member_name=zip_info.filename,
                target_path=temporary_file_path,
            )

            try:
                type = get_file_type_extension(
                    path=temporary_file_path
                )
                return type if type is not None else UnknownFileType()
            except Exception:
                return UnknownFileType()
