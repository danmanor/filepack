from pathlib import Path
from typing import Optional, final

from archive.archives.rar import RarArchive
from archive.archives.seven_zip import SevenZipArchive
from archive.archives.tar import TarArchive
from archive.archives.zip import ZipArchive
from archive.models import AbstractArchive, ArchiveMember, ArchiveType
from archive.utils import get_file_type_extension


@final
class Archive:
    def __init__(self, path: Path) -> None:
        self._path = Path(path)

        if not self._path.exists():
            try:
                self._type = ArchiveType(
                    self._path.suffix.lstrip(".")
                )
            except Exception:
                raise ValueError("given file type is not supported")

        else:
            self._type = ArchiveType(
                get_file_type_extension(path=self._path)
            )

        self._instance: AbstractArchive

        match self._type:
            case ArchiveType.TAR:
                self._instance = TarArchive(
                    path=path,
                )

            case ArchiveType.ZIP:
                self._instance = ZipArchive(
                    path=path,
                )

            case ArchiveType.RAR:
                self._instance = RarArchive(
                    path=path,
                )

            case ArchiveType.SEVEN_ZIP:
                self._instance = SevenZipArchive(
                    path=path,
                )

    def extract_member(self, target_path: Path):
        self._instance.extract_all(target_path=target_path)

    def get_members(self) -> list[ArchiveMember]:
        return self._instance.get_members()

    def add_member(self, member_path: str | Path):
        self._instance.add_member(member_path=member_path)

    def remove_member(self, member_name: str):
        self._instance.remove_member(member_name=member_name)

    def extract_all(self, target_path: str | Path):
        self._instance.extract_all(target_path=target_path)

    def remove_all(self):
        self._instance.remove_all()

    def get_member(self, member_name: str) -> Optional[ArchiveMember]:
        return self._instance.get_member(member_name=member_name)

    def get_members_name(self) -> list[str]:
        return self._instance.get_members_name()

    def print_members(self):
        self._instance.print_members()
