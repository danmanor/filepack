from enum import Enum
from abc import ABC, abstractmethod
from pathlib import Path
from tabulate import tabulate
from types import TracebackType
from typing import Optional, Type


class ArchiveType(Enum):
    TAR = ".tar"
    ZIP = ".zip"
    RAR = ".rar"
    SEVEN_ZIP = ".7z"


class FileType(Enum):
    REGULAR_FILE = "regular"
    DIRECTORY = "directory"
    UNSUPPORTED = "unsupported"


class ArchiveMember:
    def __init__(self, name: str, size: int, mtime: str, type: FileType) -> None:
        self.name = name
        self.size = size
        self.mtime = mtime
        self.type = type

    def is_regular_file(self) -> bool:
        return self._type == FileType.REGULAR_FILE

    def is_directory(self) -> bool:
        return self._type == FileType.DIRECTORY


class AbstractArchive(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        pass

    @abstractmethod
    def extract_all(self, target_path: Path):
        pass

    @abstractmethod
    def get_members(self) -> list[ArchiveMember]:
        pass

    @abstractmethod
    def add(self, path: Path):
        pass

    @abstractmethod
    def get_file_name_without_suffix(self) -> str:
        pass

    def get_member(self, name: str) -> Optional[ArchiveMember]:
        for member in self.get_members():
            if member.name == name:
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
                "type": member.type,
            }
            for member in self.get_members()
        ]
        print(tabulate(members_metadata, headers="keys", tablefmt="grid"))
