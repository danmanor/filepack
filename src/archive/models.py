from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Optional

from tabulate import tabulate

from archive.exceptions import (
    FailedToExtractArchiveMembers,
    FailedToGetArchiveMember,
    FailedToRemoveArchiveMembers,
)
from archive.utils import reraise_as


class ArchiveType(Enum):
    TAR = "tar"
    ZIP = "zip"
    RAR = "rar"
    SEVEN_ZIP = "7z"


class ArchiveMember:
    def __init__(self, name: str, size: int, mtime: str) -> None:
        self.name = name
        self.size = size
        self.mtime = mtime


class AbstractArchive(ABC):
    @property
    @abstractmethod
    def path(self) -> Path:
        pass

    @abstractmethod
    def extract_member(
        self,
        member_name: str,
        target_path: str | Path,
    ):
        pass

    @abstractmethod
    def get_members(self) -> list[ArchiveMember]:
        pass

    @abstractmethod
    def add_member(self, member_path: str | Path):
        pass

    @abstractmethod
    def remove_member(self, member_name: str):
        pass

    @reraise_as(FailedToExtractArchiveMembers)
    def extract_all(self, target_path: str | Path):
        for member in self.get_members():
            self.extract_member(
                member_name=member.name, target_path=target_path
            )

    @reraise_as(FailedToRemoveArchiveMembers)
    def remove_all(self):
        for member in self.get_members():
            self.remove_member(member=member)

    @reraise_as(FailedToGetArchiveMember)
    def get_member(self, member_name: str) -> Optional[ArchiveMember]:
        for member in self.get_members():
            if member.name == member_name:
                return member
        return None

    def get_members_name(self) -> list[str]:
        return [member.name for member in self.get_members()]

    def print_members(self):
        members_metadata = [
            {
                "name": member.name,
                "mtime": member.mtime,
                "size": member.size,
            }
            for member in self.get_members()
        ]
        print(
            tabulate(
                members_metadata, headers="keys", tablefmt="grid"
            )
        )
