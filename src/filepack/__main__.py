"""A user-friendly interface for handling files, archives, and compressed files
in Python.

Usage:     
    filepack    archive         (-t <type> | --type=<type>) 
                                [-d <dst> | --dst=<dst>]
                                [-i | --in-place]
                                <file>...     
    filepack    extract         [-d<dst> | --dst=<dst>]
                                <archive-path>
    filepack    compress        (-t <type> | --type=<type>) 
                                [-i | --in-place] 
                                [-d<dst> | --dst=<dst>] 
                                [-l <level> | --level=<level>] 
                                <file-path> 
    filepack    decompress      (-t <type> | --type=<type>) 
                                [-i | --in- place]
                                [-d <dst> | --dst=<dst>] 
                                <file-path> 
    filepack                    (-h | --help)     
    filepack                    (-v | --version)

Options:     
    -h, --help                      Show this screen.     
    -v, --version                   Show version.     
    -t, --type=<type>               Archive/compression type.     
    -d, --dst=<dst>                 The path of the new archive/compression.     
    -l, --level=<level>             Compression level.
    -i, --in-place                  Replace the file with its new compression.
"""
import sys
from pathlib import Path

import docopt
import toml  # type: ignore

from filepack import FilePack
from filepack.archives.models import ArchiveType
from filepack.compressions.models import CompressionType


def archive_files(
    file_paths: list[Path], destination_path: Path, in_place: bool
):
    try:
        for file_path in file_paths:
            file_pack = FilePack(destination_path)
            file_pack.add_member(member_path=file_path, in_place=in_place)
    except Exception as e:
        print(f"An error occurred while archiving files: {e}")
        sys.exit(1)


def extract_files(archive_path: Path, destination_path: Path, in_place: bool):
    try:
        file_pack = FilePack(archive_path)
        file_pack.extract_all(target_path=destination_path, in_place=in_place)
    except Exception as e:
        print(f"An error occurred while archiving files: {e}")
        sys.exit(1)


def compress_file(
    file_path: Path,
    destination_path: Path,
    compression_algorithm: CompressionType,
    compression_level: int,
    in_place: bool,
):
    try:
        file_pack = FilePack(file_path)
        file_pack.compress(
            compression_algorithm=compression_algorithm,
            target_path=destination_path,
            compression_level=compression_level,
            in_place=in_place,
        )
    except Exception as e:
        print(f"An error occurred while compressing files: {e}")
        sys.exit(1)


def decompress_file(
    file_paths: list[Path],
    destination_path: Path,
    compression_type: CompressionType,
    in_place: bool,
):
    try:
        for file_path in file_paths:
            file_pack = FilePack(file_path)
            file_pack.decompress(
                compression_algorithm=compression_type,
                target_path=destination_path,
                in_place=in_place,
            )

    except Exception as e:
        print(f"An error occurred while compressing files: {e}")
        sys.exit(1)


def get_package_version():
    config_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(config_path, "r") as pyproject:
        file_contents = pyproject.read()

    pyproject_data = toml.loads(file_contents)
    return pyproject_data["project"]["version"]


def main():
    arguments = docopt.docopt(__doc__, version=get_package_version())

    if arguments["archive"]:
        file_paths = [Path(file) for file in arguments["<file>"]]
        archive_type = ArchiveType(arguments["--type"].lower()).value
        in_place = arguments["--in-place"]
        destination_path = arguments["--dst"]
        if destination_path is None:
            destination_path = Path.cwd() / f"archive.{archive_type}"

        else:
            destination_path = Path(destination_path)

        if destination_path.suffix.lstrip(".") != archive_type:
            raise ValueError(
                f"for archive of the type you specified, please provide a destination path which ends with '{archive_type}'"
            )

        archive_files(
            file_paths=file_paths,
            destination_path=destination_path,
            in_place=in_place,
        )

    if arguments["extract"]:
        destination_path = arguments["--dst"]
        archive_path = Path(arguments["<archive-path>"])
        in_place = arguments["--in-place"]

        if destination_path is None:
            destination_path = archive_path.parent

        else:
            destination_path = Path(destination_path)

        if not destination_path.exists():
            destination_path.mkdir()

        elif not destination_path.is_dir():
            raise ValueError("destination path must be a directory")

        extract_files(
            archive_path=archive_path,
            destination_path=destination_path,
            in_place=in_place,
        )

    if arguments["compress"]:
        compression_algorithm = CompressionType(arguments["--type"].lower())
        in_place = arguments["--in-place"]
        file_path = Path(arguments["<file-path>"])
        destination_path = arguments["--dst"]
        if destination_path is None:
            destination_path = (
                file_path.parent
                / f"{file_path.name}.{compression_algorithm.value}"
            )

        compression_level = (
            9 if arguments["--level"] is None else int(arguments["--level"])
        )

        compress_file(
            file_path=file_path,
            destination_path=destination_path,
            compression_algorithm=compression_algorithm,
            compression_level=compression_level,
            in_place=in_place,
        )

    if arguments["decompress"]:
        compression_algorithm = CompressionType(arguments["--type"].lower())
        in_place = arguments["--in-place"]
        destination_path = arguments["--dst"]
        file_path = Path(arguments["<file-path>"])
        if destination_path is None:
            try:
                suffix = CompressionType(file_path.suffix)
                if suffix.value.lstrip(".") == compression_algorithm:
                    destination_path = file_path.parent / file_path.stem
                else:
                    destination_path = file_path.parent / Path(
                        f"{file_path.stem}_decsompressed.{file_path.suffix}"
                    )

            except Exception:
                destination_path = file_path.parent / Path(
                    f"{file_path.stem}_decsompressed.{file_path.suffix}"
                )

        else:
            destination_path = file_path.parent / Path(
                f"{file_path.stem}_decsompressed.{file_path.suffix}"
            )

        decompress_file(
            file_path=file_path,
            destination_path=destination_path,
            compression_algorithm=compression_algorithm,
            in_place=in_place,
        )


if __name__ == "__main__":
    main()
