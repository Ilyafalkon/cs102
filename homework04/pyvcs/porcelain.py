import os
import pathlib
import typing as tp
import zlib

from pyvcs.index import read_index, update_index
from pyvcs.objects import (commit_parse, find_object, find_tree_files,
                           read_object, read_tree)
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths, True)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir))
    return commit_tree(gitdir, tree, message, author=author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    index = read_index(gitdir)
    for entry in index:
        if os.path.exists(entry.name):
            if "/" in entry.name:
                os.remove(entry.name)
                os.rmdir(entry.name[: entry.name.index("/")])
            else:
                os.remove(entry.name)
    with (gitdir / "objects" / obj_name[:2] / obj_name[2:]).open("rb") as f:
        data = f.read()
    tree_sha = commit_parse(data).decode()
    for entry in find_tree_files(tree_sha, gitdir):
        if "/" in entry[0]:
            dir_name = entry[0][: entry[0].index("/")]
            os.mkdir(dir_name)
        _, data = read_object(entry[1], gitdir)
        with (pathlib.Path(entry[0])).open('w') as f: #type: ignore
            f.write(data.decode()) #type: ignore 