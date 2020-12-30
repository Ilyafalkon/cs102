import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    refdir = gitdir / get_ref(gitdir)
    with refdir.open("w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    ...


def ref_resolve(gitdir: pathlib.Path, refname: str) -> tp.Optional[str]:
    if refname == "HEAD":
        return resolve_head(gitdir)
    elif (gitdir / refname).exists():
        with (gitdir / refname).open("r") as f:
            data = f.read()
    return data


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    refdir = gitdir / get_ref(gitdir)
    if not refdir.exists():
        return None
    with refdir.open("r") as f:
        data = f.read()
    return data


def is_detached(gitdir: pathlib.Path) -> bool:
    try:
        get_ref(gitdir)
    except:
        return True
    return False


def get_ref(gitdir: pathlib.Path) -> str:
    with (gitdir / "HEAD").open("r") as f:
        refname = f.read().strip()
    refname = refname[refname.index(" ") + 1 :]
    return refname
