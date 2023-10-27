from pathlib import Path
from typing import Optional, final

from filepack.archives.exceptions import (
    FailedToAddNewMemberToArchive,
    FailedToExtractArchiveMember,
    FailedToExtractArchiveMembers,
    FailedToGetArchiveMember,
    FailedToGetArchiveMembers,
    FailedToRemoveArchiveMember,
    FailedToRemoveArchiveMembers,
)
from filepack.archives.models import (
    AbstractArchive,
    ArchiveMember,
    ArchiveType,
)
from filepack.archives.rar import RarArchive
from filepack.archives.seven_zip import SevenZipArchive
from filepack.archives.tar import TarArchive
from filepack.archives.zip import ZipArchive
from filepack.consts import ERROR_MESSAGE_NOT_SUPPORTED
from filepack.utils import get_file_type_extension, reraise_as


@final
class Archive:
    def __init__(self, path: Path) -> None:
        self._path = Path(path)

        if not self._path.exists():
            try:
                self._type = ArchiveType(self._path.suffix.lstrip("."))
            except Exception:
                raise ValueError(ERROR_MESSAGE_NOT_SUPPORTED)

        else:
            self._type = ArchiveType(get_file_type_extension(path=self._path))

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

    @property
    def path(self) -> Path:
        return self._path

    @property
    def suffix(self) -> str:
        return self._type.value

    @reraise_as(FailedToExtractArchiveMember)
    def extract_member(self, target_path: Path):
        self._instance.extract_all(target_path=target_path)

    @reraise_as(FailedToGetArchiveMembers)
    def get_members(self) -> list[ArchiveMember]:
        return self._instance.get_members()

    @reraise_as(FailedToAddNewMemberToArchive)
    def add_member(self, member_path: str | Path):
        self._instance.add_member(member_path=member_path)

    @reraise_as(FailedToRemoveArchiveMember)
    def remove_member(self, member_name: str):
        self._instance.remove_member(member_name=member_name)

    @reraise_as(FailedToExtractArchiveMembers)
    def extract_all(self, target_path: str | Path):
        self._instance.extract_all(target_path=target_path)

    @reraise_as(FailedToRemoveArchiveMembers)
    def remove_all(self):
        self._instance.remove_all()

    @reraise_as(FailedToGetArchiveMember)
    def get_member(self, member_name: str) -> Optional[ArchiveMember]:
        return self._instance.get_member(member_name=member_name)

    @reraise_as(FailedToGetArchiveMembers)
    def get_members_name(self) -> list[str]:
        return self._instance.get_members_name()

    @reraise_as(FailedToGetArchiveMembers)
    def print_members(self):
        self._instance.print_members()
