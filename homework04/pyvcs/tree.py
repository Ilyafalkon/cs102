import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    line = b""
    for entry in index:
        if "/" in entry.name:
            line += b"40000 "
            subdir = b""
            dir_name = entry.name[: entry.name.find("/")]
            line += dir_name.encode() + b"\0"
            subdir += oct(entry.mode)[2:].encode() + b" "
            subdir += entry.name[entry.name.find("/") + 1 :].encode() + b"\0"
            subdir += entry.sha1
            blob_hash = hash_object(subdir, fmt="tree", write=True)
            line += bytes.fromhex(blob_hash)
        else:
            line += oct(entry.mode)[2:].encode() + b" "
            line += entry.name.encode() + b"\0"
            line += entry.sha1
    return hash_object(line, fmt="tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    seconds_time = int(time.mktime(time.localtime()))
    timezone_check = time.timezone
    if timezone_check > 0:
        timezone = "-"
    else:
        timezone = "+"
    timezone += f"{abs(timezone_check) // 3600:02}00"
    if author is None:
        author = f'{os.getenv("GIT_AUTHOR_NAME")}  {os.getenv("GIT_AUTHOR_EMAIL")}'
    if parent is None:
        data = f"tree {tree}\nauthor {author} {seconds_time} {timezone}\ncommitter {author} {seconds_time} {timezone}\n\n{message}\n"
    else:
        data = f"tree {tree}\nparent {parent}\nauthor {author} {seconds_time} {timezone}\ncommitter {author} {seconds_time} {timezone}\n\n{message}\n"
    return hash_object(data.encode(), fmt="commit", write=True)
