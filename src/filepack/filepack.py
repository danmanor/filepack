from pathlib import Path
from typing import Optional

from filepack.archive import Archive
from filepack.archives.models import ArchiveMember
from filepack.compression import Compression
from filepack.utils import ensure_instance


class FilePack:
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

        try:
            self._archive_instance = Archive(path=self._path)
        except Exception:
            pass

        try:
            self._compression_instance = Compression(path=self._path)
        except Exception:
            pass

        if (
            getattr(self, "_archive_instance", None) is None
            and getattr(self, "_compression_instance", None) is None
        ):
            raise ValueError()

    @property
    def path(self) -> Path:
        return self._path

    @property
    def suffix(self) -> str:
        return self.path.suffix.lstrip(".")

    @property
    @ensure_instance("_compression_instance")
    def uncompressed_size(self) -> int:
        return self._compression_instance.uncompressed_size

    @property
    @ensure_instance("_compression_instance")
    def compressed_size(self) -> int:
        return self._compression_instance.compressed_size

    @property
    @ensure_instance("_compression_instance")
    def compression_ratio(self) -> str:
        return self._compression_instance.compression_ratio

    @ensure_instance("_archive_instance")
    def extract_member(self, target_path: Path):
        self._archive_instance.extract_all(target_path=target_path)

    @ensure_instance("_archive_instance")
    def get_members(self) -> list[ArchiveMember]:
        return self._archive_instance.get_members()

    @ensure_instance("_archive_instance")
    def add_member(self, member_path: str | Path):
        self._archive_instance.add_member(member_path=member_path)

    @ensure_instance("_archive_instance")
    def remove_member(self, member_name: str):
        self._archive_instance.remove_member(member_name=member_name)

    @ensure_instance("_archive_instance")
    def extract_all(self, target_path: str | Path):
        self._archive_instance.extract_all(target_path=target_path)

    @ensure_instance("_archive_instance")
    def remove_all(self):
        self._archive_instance.remove_all()

    @ensure_instance("_archive_instance")
    def get_member(self, member_name: str) -> Optional[ArchiveMember]:
        return self._archive_instance.get_member(
            member_name=member_name
        )

    @ensure_instance("_archive_instance")
    def get_members_name(self) -> list[str]:
        return self._archive_instance.get_members_name()

    @ensure_instance("_archive_instance")
    def print_members(self):
        self._archive_instance.print_members()

    @ensure_instance("_compression_instance")
    def decompress(self, target_path: str | Path):
        self._compression_instance.decompress(target_path=target_path)

    @ensure_instance("_compression_instance")
    def compress(
        self,
        target_path: Path = Path.cwd(),
        compression_level: int = 9,
    ):
        self._compression_instance.compress(
            target_path=target_path,
            compression_level=compression_level,
        )

    @ensure_instance("_compression_instance")
    def is_compressed(self) -> bool:
        return self._compression_instance.is_compressed()
