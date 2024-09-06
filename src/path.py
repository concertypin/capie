import os


class BasePath:
    path: str

    def __init__(self, path: str):
        self.path = path

    def __add__(self, other: "str|Path") -> "Path":
        if isinstance(other, Path):
            return Path(os.path.join(self.path, other.path))
        else:
            return Path(os.path.join(self.path, other))

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return self.__str__()


class Dir:
    path: str

    def is_dir(self) -> bool:
        return os.path.isdir(self.path)

    def list(self) -> "list[Path]":
        return [Path(self.path) + Path(i) for i in os.listdir(self.path)]


class File:
    path: str

    def is_file(self) -> bool:
        return os.path.isfile(self.path)

    def name(self) -> str:
        return os.path.basename(self.path)

    def absolute(self) -> str:
        return os.path.abspath(self.path)


class Readable:
    path: str

    def open(self, mode: str, **kwargs):
        return open(self.path, mode, **kwargs)

    def read(self) -> str:
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def read_binary(self) -> bytes:
        with open(self.path, "rb") as f:
            return f.read()


class Path(BasePath, Readable, Dir, File):
    pass
