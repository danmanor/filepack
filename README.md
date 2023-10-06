# filepack

A user-friendly interface for handling files, archives, and compressed files in Python.

## Features

- User-friendly interface for common file operations.
- Support for various archive types: TAR, ZIP, RAR, SEVEN_ZIP.
- Support for various compression types: GZIP, BZ2, LZ4, XZ.

## Installation
```
pip install filepack
```

## API Overview


### FilePack

| Method/Property       | Description                                     |
|-----------------------|-------------------------------------------------|
| `path`                | Returns the path of the file.                   |
| `suffix`              | Returns the file's suffix.                      |
| `is_compressed`       | Check if the file is compressed.                |
| `uncompressed_size`   | Get uncompressed size.                          |
| `compressed_size`     | Get compressed size.                            |
| `compression_ratio`   | Get compression ratio.                          |
| `compress`            | Compress the file.                              |
| `decompress`          | Decompress the file.                            |

### Archive

| Method/Property       | Description                                     |
|-----------------------|-------------------------------------------------|
| `path`                | Returns the path of the archive.                |
| `suffix`              | Returns the archive's suffix.                   |
| `extract_member`      | Extract a specific member.                      |
| `get_members`         | Get a list of members.                          |
| `add_member`          | Add a member to the archive.                    |
| `remove_member`       | Remove a member from the archive.               |
| `extract_all`         | Extract all members.                            |
| `remove_all`          | Remove all members from the archive.            |
| `print_members`       | Print all members.                              |

### Compression

| Method/Property       | Description                                     |
|-----------------------|-------------------------------------------------|
| `path`                | Returns the path of the compressed file.        |
| `suffix`              | Returns the file's suffix.                      |
| `uncompressed_size`   | Get uncompressed size.                          |
| `compressed_size`     | Get compressed size.                            |
| `compression_ratio`   | Get compression ratio.                          |
| `compress`            | Compress the file.                              |
| `decompress`          | Decompress the file.                            |
| `is_compressed`       | Check if the file is compressed.                |

## Usage

### Working with Files

```
from filepack import FilePack

pack = FilePack("path/to/your/file")

# Check if the file is compressed
is_compressed = pack.is_compressed()


# Get uncompressed size
size = pack.uncompressed_size


# Compress and decompress files
pack.compress(target_path="path/to/compressed/file")
pack.decompress(target_path="path/to/uncompressed/file")
```

### Working with Archives

```
from filepack import Archive

archive = Archive("path/to/archive")

# Extract a specific member
archive.extract_member(target_path="path/to/target")

# Get a list of members
members = archive.get_members()

# Add a member to the archive
archive.add_member("path/to/member")

# Remove a member from the archive
archive.remove_member("name_of_member")

# Extract all members
archive.extract_all(target_path="path/to/target")

# Remove all members from the archive
archive.remove_all()

# Print all members
archive.print_members()
```

### Working with Compressions

```
from filepack import Compression

compression = Compression("path/to/compressed_file")

# Get compressed size
compressed_size = compression.compressed_size

# Get compression ratio
ratio = compression.compression_ratio

# Compress and decompress files
compression.compress(target_path="path/to/compressed/file")
compression.decompress(target_path="path/to/uncompressed/file")
```

## Error Handling

`filepack` has built-in error handling mechanisms. It raises user-friendly exceptions for common errors, allowing you to handle them gracefully in your application.

## Contributing

Interested in contributing to `filepack`? [See our contribution guide](CONTRIBUTING.md).

