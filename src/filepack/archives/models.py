from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Optional

from tabulate import tabulate

from filepack.archives.consts import (
    RAR_SUFFIX,
    SEVEN_ZIP_SUFFIX,
    TAR_SUFFIX,
    ZIP_SUFFIX,
)


class ArchiveType(Enum):
    TAR = TAR_SUFFIX
    ZIP = ZIP_SUFFIX
    RAR = RAR_SUFFIX
    SEVEN_ZIP = SEVEN_ZIP_SUFFIX


class UnknownFileType:
    pass


class ArchiveMember:
    def __init__(
        self,
        name: str,
        size: int,
        mtime: str,
        type: str | UnknownFileType,
    ) -> None:
        self.name = name
        self.size = size
        self.mtime = mtime
        self.type = type


class AbstractArchive(ABC):
    def __init__(self, path: Path, extension: str) -> None:
        self._path = path
        self._suffix = path.suffix.lstrip(".")
        self._dot_suffix = path.suffix
        self._extension = extension

    @abstractmethod
    def get_members(self) -> list[ArchiveMember]:
        pass

    @abstractmethod
    def add_member(self, member_path: str | Path):
        pass

    @abstractmethod
    def remove_member(self, member_name: str):
        pass

    @abstractmethod
    def get_member(self, member_name: str) -> Optional[ArchiveMember]:
        pass

    @abstractmethod
    def member_exist(self, member_name: str) -> bool:
        pass

    @abstractmethod
    def extract_member(
        self,
        member_name: str,
        target_path: str | Path,
    ):
        pass

    def extract_all(self, target_path: str | Path):
        for member in self.get_members():
            self.extract_member(
                member_name=member.name, target_path=target_path
            )

    def remove_all(self):
        for member_name in self.get_members_name():
            self.remove_member(member_name=member_name)

    def get_members_name(self) -> list[str]:
        return [member.name for member in self.get_members()]

    def print_members(self):
        members_metadata = [
            {
                "name": member.name,
                "mtime": member.mtime,
                "size": member.size,
                "type": member.type,
            }
            for member in self.get_members()
        ]
        print(tabulate(members_metadata, headers="keys", tablefmt="grid"))
