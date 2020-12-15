import hashlib
import operator
import os
import pathlib
import struct
import typing as tp
from typing import List

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        values = (
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino & 0xFFFFFFFF,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
        )
        packed = struct.pack("!LLLLLLLLLL20sH", *values)
        name = self.name.encode()
        N = 8 - (62 + len(name)) % 8
        return packed + name + b"\x00" * N

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        data_wo_name = data[:62]
        unpacked = struct.unpack("!LLLLLLLLLL20sH", data_wo_name)
        counter = 0
        new_data = data[62:]
        for symbol in new_data:
            if symbol != 0:
                counter += 1
            else:
                break
        name = new_data[:counter].decode()
        return GitIndexEntry(
            ctime_s=unpacked[0],
            ctime_n=unpacked[1],
            mtime_s=unpacked[2],
            mtime_n=unpacked[3],
            dev=unpacked[4],
            ino=unpacked[5],
            mode=unpacked[6],
            uid=unpacked[7],
            gid=unpacked[8],
            size=unpacked[9],
            sha1=unpacked[10],
            flags=unpacked[11],
            name=name,
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    entries: List[GitIndexEntry] = []
    indexdir = gitdir / "index"
    if indexdir.exists():
        with indexdir.open("rb") as f:
            data = f.read()
    else:
        return entries
    signature = b"DIRC"
    version = 2
    needed_range = struct.unpack("!L", data[8:12])[0]
    header = struct.pack("!4sLL", signature, version, needed_range)
    new_data = data[len(header) :]
    for i in range(needed_range):
        counter = 0
        zero_counter = 0
        for symbol in new_data[62:]:
            if symbol != 0:
                if zero_counter > 0:
                    break
                counter += 1
            else:
                zero_counter += 1
        entry = GitIndexEntry.unpack(new_data)
        entries.append(entry)
        new_data = new_data[62 + zero_counter + counter :]
        if len(new_data) < 64:
            break
    return entries


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    index = gitdir / "index"
    packed_entries = ""
    for entry in entries:
        packed_entries += bytes.hex(entry.pack())
    signature = b"DIRC"
    version = 2
    header = struct.pack("!4sLL", signature, version, len(entries))
    data = header + bytes.fromhex(packed_entries)
    with index.open("wb") as f:
        f.write(data + hashlib.sha1(data).digest())


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    entries = read_index(gitdir)
    for entry in entries:
        if details == False:
            print(entry.name)
        else:
            stage = (entry.flags >> 12) & 3
            print(f"{entry.mode:o} {bytes.hex(entry.sha1)} {stage}\t{entry.name}")


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = []
    paths = sorted(paths)
    for path in paths:
        with path.open("rb") as f:
            data = f.read()
        sha = hash_object(data, fmt="blob", write=True)
        entry = GitIndexEntry(
            ctime_s=int(os.stat(path).st_ctime),
            ctime_n=0,
            mtime_s=int(os.stat(path).st_mtime),
            mtime_n=0,
            dev=os.stat(path).st_dev,
            ino=os.stat(path).st_ino,
            mode=os.stat(path).st_mode,
            uid=os.stat(path).st_uid,
            gid=os.stat(path).st_gid,
            size=os.stat(path).st_size,
            sha1=bytes.fromhex(sha),
            flags=len(path.name),
            name=str(path),
        )
        entries.append(entry)
    if write:
        if not (gitdir / "index").exists():
            write_index(gitdir, entries)
        else:
            index = read_index(gitdir)
            index += entries
            write_index(gitdir, index)
