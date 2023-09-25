from pathlib import Path
from archive.archive import Archive
import pytest
from archive.exceptions import (
    FailedToAddNewMemberToArchive,
    FailedToGetArchiveMembers
)

@pytest.fixture
def file(tmp_path):
    new_file_path = tmp_path / "new_file.txt"
    with open(new_file_path, "w") as new_file:
        new_file.write("Hello World !")
    
    return new_file_path

ARCHIVES_PATH = Path(__file__).parent / "archive_examples"

def test_tar_archive(tmp_path, file):
    new_tar_path = tmp_path / "new_tar.tar"

    arc = Archive(new_tar_path)
    arc.add_member(file)

    assert len(arc.get_members()) == 1
    assert arc.get_member("new_file.txt") is not None
    
    extraction_path = tmp_path / "extracted"
    arc.extract_all(extraction_path)

    assert (extraction_path / "new_file.txt").read_text() == "Hello World !"
    
    arc.remove_member(member_name="new_file.txt")

    assert arc.get_member(member_name="new_file.txt") is None

    arc = Archive(ARCHIVES_PATH / "archive.tar")

    assert [member.name for member in arc.get_members()] == ["a.txt", "b.txt"]
    


def test_zip_archive(tmp_path, file):
    new_tar_path = tmp_path / "new_tar.tar"

    arc = Archive(new_tar_path)
    arc.add_member(file)

    assert len(arc.get_members()) == 1
    assert arc.get_member("new_file.txt") is not None
    
    extraction_path = tmp_path / "extracted"
    arc.extract_all(extraction_path)

    assert (extraction_path / "new_file.txt").read_text() == "Hello World !"
    
    arc.remove_member(member_name="new_file.txt")

    assert arc.get_member(member_name="new_file.txt") is None

    arc = Archive(ARCHIVES_PATH / "archive.zip")

    assert [member.name for member in arc.get_members()] == ["a.txt", "b.txt"]


def test_7zip_archive(tmp_path, file):
    new_tar_path = tmp_path / "new_tar.tar"

    arc = Archive(new_tar_path)
    arc.add_member(file)

    assert len(arc.get_members()) == 1
    assert arc.get_member("new_file.txt") is not None
    
    extraction_path = tmp_path / "extracted"
    arc.extract_all(extraction_path)

    assert (extraction_path / "new_file.txt").read_text() == "Hello World !"
    
    arc.remove_member(member_name="new_file.txt")

    assert arc.get_member(member_name="new_file.txt") is None

    arc = Archive(ARCHIVES_PATH / "archive.7z")

    assert [member.name for member in arc.get_members()] == ["a.txt", "b.txt"]


def test_rar_archive(tmp_path, file):
    new_rar_path = tmp_path / "new_rar.rar"

    arc = Archive(new_rar_path)
    
    with pytest.raises(FailedToAddNewMemberToArchive):
        arc.add_member(file)

    with pytest.raises(FailedToGetArchiveMembers):  # archive does not exist
        arc.get_members()
    
    arc = Archive(ARCHIVES_PATH / "archive.rar")

    assert len(arc.get_members()) == 1
    assert arc.get_member("sample-1_1.webp") is not None

    with pytest.raises(FailedToAddNewMemberToArchive):
        arc.add_member(file)
    