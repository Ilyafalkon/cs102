import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    workdir = workdir.absolute()
    gitdir = workdir / os.environ["GIT_DIR"]
    while not gitdir.exists() and gitdir.parent != pathlib.Path("/"):
        gitdir = gitdir.parent.parent / os.environ["GIT_DIR"]
    if gitdir.exists():
        return gitdir
    else:
        raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    gitdir = workdir / os.environ["GIT_DIR"]
    try:
        gitdir.mkdir(parents=True)
    except:
        raise Exception(f"{workdir} is not a directory")
    pathlib.Path(os.path.join(gitdir, "refs", "tags")).mkdir(parents=True)
    pathlib.Path(os.path.join(gitdir, "refs", "heads")).mkdir(parents=True)
    pathlib.Path(os.path.join(gitdir, "objects")).mkdir(parents=True)
    head = pathlib.Path(gitdir / "HEAD")
    with head.open("w") as f:
        f.write("ref: refs/heads/master\n")
    config = pathlib.Path(gitdir / "config")
    with config.open("w") as f:
        f.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
        )
    description = pathlib.Path(gitdir / "description")
    with description.open("w") as f:
        f.write("Unnamed pyvcs repository.\n")
    return gitdir
