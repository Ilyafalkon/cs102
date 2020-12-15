import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find

os.environ["GIT_DIR"] = ".git"


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    hash_of_object = hashlib.sha1(store).hexdigest()
    if write:
        hashdir = repo_find(".") / "objects" / hash_of_object[:2]
        if not hashdir.exists():
            hashdir.mkdir(parents=True)
            compressed_zlib = zlib.compress(store)
            with (hashdir / hash_of_object[2:]).open("wb") as f:
                f.write(compressed_zlib)
    return hash_of_object


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    objects = []
    objectdir = gitdir / "objects" / obj_name[:2]
    if len(obj_name) == 5:
        if objectdir.exists():
            for file in os.listdir(path=objectdir):
                if obj_name[2:] in file:
                    obj = obj_name[:2] + file
                    objects.append(obj)
    else:
        raise Exception(f"Not a valid object name {obj_name}")
    if len(objects) == 0:
        raise Exception(f"Not a valid object name {obj_name}")
    return objects


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    objectdir = gitdir / "objects" / sha[:2] / sha[2:]
    with objectdir.open("rb") as f:
        store = zlib.decompress(f.read())
    fmt = store[: store.index(b"\x00")]
    fmt = fmt[: fmt.index(b" ")]
    data = store[store.index(b"\x00") + 1 :]
    return (fmt.decode(), data)


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    output = []
    while len(data) != 0:
        mode = int(data[: data.index(b" ")].decode())
        data = data[data.index(b" ") + 1 :]
        sha = data[: data.index(b"\x00")].decode()
        data = data[data.index(b"\x00") + 1 :]
        name = bytes.hex(data[:20])
        data = data[20:]
        output.append((mode, sha, name))
    return output


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find(".")
    fmt, data = read_object(obj_name, gitdir)
    if fmt == "blob" or fmt == "commit":
        print(data.decode())
    else:
        for entry in read_tree(data):
            if entry[0] == 40000:
                fmts = "tree"
            else:
                fmts = "blob"
            print(f"{entry[0]:06} {fmts} {entry[2]}\t{entry[1]}")


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    tree_files = []
    _, data = read_object(tree_sha, gitdir)
    for entry in read_tree(data):
        if read_object(entry[2], gitdir)[0] == "tree":
            tree = find_tree_files(entry[2], gitdir)
            for blob in tree:
                name = entry[1] + "/" + blob[0]
                tree_files.append((name, blob[1]))
        else:
            tree_files.append((entry[1], entry[2]))
    return tree_files


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    start = data.index(b"tree") + 5
    return data[start : start + 40]
