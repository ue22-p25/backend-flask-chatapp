#!/usr/bin/env python

"""
A tool for managing a set of steps, as either a git repository or a folder hierarchy
"""

import sys
import re
from os import chdir
from pathlib import Path
import subprocess as sp
from itertools import count

import logging
logger = logging.getLogger('steps')
logging.basicConfig(level=logging.INFO)

(debug, info, warning, error) = logger.debug, logger.info, logger.warning, logger.error

import click


COMMIT_RE = r"step (?P<step>\w+) - (?P<message>.+)"
HASH_COMMIT_RE = r"(?P<hash>[0-9a-f]+) " + COMMIT_RE
README_RE = r"# (?P<message>.+)"

COMMIT_MATCHER = re.compile("^"+COMMIT_RE+"$")
HASH_COMMIT_MATCHER = re.compile("^"+HASH_COMMIT_RE+"$")
README_MATCHER = re.compile("^"+README_RE+"$")

DOTSTEPS = ".steps"


def shell(command: str, **kwds) -> sp.CompletedProcess:
    debug(f"running command: {command}")
    completed = sp.run(command, shell=True, **kwds)
    # if completed.returncode != 0:
    #     error(f"WHOOOPS - Command failed: {command}")
    return completed

def shell_silent(command: str, **kwds) -> sp.CompletedProcess:
    return shell(command, stdout=sp.DEVNULL, stderr=sp.DEVNULL, **kwds)

def shell_capture(command: str, **kwds) -> sp.CompletedProcess:
    completed = shell(command, capture_output=True, **kwds)
    return completed.stdout.decode().strip()


# temporary
def retrieve_message_from_commit(repo, step, branch):
    """
    normally the one-liner attached to a step is in step.md
    however as a last resort
    when bootstrapping from a git repository
    we may find the message in the log messages
    """
    command = f"git -C {repo} log --oneline {branch} --grep='step {step} -'"
    line = shell_capture(command)
    if match := COMMIT_MATCHER.match(line):
        return match.group('step'), match.group("message")
    return "unknown", "cannot find message"


def retrieve_message_from_step_md(repo):
    step_md_file = repo / "step.md"
    if not step_md_file.exists():
        warning(f"!! {step_md_file} does not exist")
        return "unknown", "cannot find message"
    with step_md_file.open() as f:
        content = f.read()
        if match := README_MATCHER.match(content):
            return None, match.group("message")
        else:
            warning(f"!!! WARNING !!! {step_md_file} not understood")
            warning(content)
            warning(f"!!! WARNING !!! {step_md_file} end")

    return None, "cannot find message"


# temporary
def strip_docstring(path: Path) -> str:
    """
    rewrites file without its docstring if it occurs is on the first line
    if present, the second line (the fist line in the docstring)
    is returned as a message
    """

    lines = []
    with path.open('r') as f:
        message = ''
        # do we need to write
        state = True
        for lineno, line in enumerate(f, 1):
            match lineno:
                case 1:
                    # not a starting doctring - nothing to do here
                    if not (line.startswith('"""') or line.startswith("'''")):
                        return ''
                    state = False
                case _:
                    if state:
                        lines.append(line)
                    if (not state) and (line.startswith('"""') or line.startswith("'''")):
                        state = 1
            if lineno == 2:
                message = line.strip()

    with Path(path).open('w') as f:
        for line in lines:
            f.write(line)
    return message


def free_branchname(repo: Path, branch_name: str) -> str:
    """
    returns a free branch name
    """
    completed = shell(f"git -C {repo} show-ref {branch_name}")
    if completed.returncode != 0:
        return branch_name
    for c in count(1):
        alt = f"{branch_name}-{c}"
        completed = shell(f"git -C {repo} show-ref {alt}")
        if completed.returncode != 0:
            return alt


@click.group(chain=True, help=sys.modules[__name__].__doc__)
@click.option("--debug", is_flag=True, help="enable debug output")
@click.option("--quiet", is_flag=True, help="enable debug output")
def cli(debug, quiet):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    if quiet:
        logging.getLogger().setLevel(logging.WARNING)


# 0 means success and anything else means failure
ShellSuccess = int


@cli.command('togit', help="rebuild a git branch from a folder hierarchy")
@click.option('-b', '--branch-name', type=str, default="steps", help="branch name to use - will search for a free one")
@click.option('-i', '--input-steps-folder', type=Path, default=None, help="use a separate steps folder")
@click.argument('repo', type=Path)

def togit(branch_name, input_steps_folder, repo: Path) -> ShellSuccess:
    """
    this rebuilds the git repository from a folder hierarchy
    """
    # by default the folder hierarchy is expected to be in the .steps directory
    if input_steps_folder is None:
        input_steps_folder = repo / DOTSTEPS

    # if there are files known to git in this folder, use the 'only_git'
    # policy, i.e. consider only git files when creating commits
    known_files = shell_capture(f"git -C {input_steps_folder} ls-files")
    only_git = True if known_files else False

    if not input_steps_folder.exists():
        error(f"Repository {input_steps_folder} does not exist.")
        return 1

    if not repo.is_dir():
        repo.mkdir(parents=True)

    input_steps_folder = input_steps_folder.absolute()

    chdir(repo)
    repo = Path(".")
    info(f"working in {repo.absolute()}")

    if Path(".git").is_dir():
        info(f"{repo} already a git repository.")
        branch_name = free_branchname(repo, branch_name)
        info(f"using branch {branch_name}")
        shell_silent(f"git switch --orphan {branch_name}")
    else:
        info(f"Creating git repository in {repo}")
        shell(f"git init --initial-branch={branch_name}")

    debug(f"globbing in {input_steps_folder}")
    steps = sorted([ step_dir.relative_to(input_steps_folder) for step_dir in input_steps_folder.glob("[0-9]*") ])
    debug(f"found {len(steps)} step directories")

    for step in steps:
        step_path = input_steps_folder / step
        info(f"Processing {step}")
        # gather all files in the directory
        if only_git:
            completed = shell(f"git -C {step_path} ls-files", capture_output=True)
            files_list = completed.stdout.decode().splitlines()
        else:
            files_list = [
                glob.relative_to(step_path) for glob in step_path.glob("**/*")
            ]

        files_list = [file for file in files_list if (step_path/file).is_file()]
        files_str = " ".join(str(file) for file in files_list)
        info(f"found {len(list(files_list))} files")
        for file in files_list:
            debug(f"  {file}")
        # xxx need to remove lingering files ?
        # we have seen e.g. app.py~ and _pycache__ files after trying out something in there...
        # the solution might be with having a .gitignore despite all...
        debug(f"{step=} {step_path=} {files_str=}")
        completed = shell( f"tar -C {step_path} -cf - {files_str} | tar -C {repo.absolute()} -xf -")
        # message = strip_docstring(Path("main.py"))
        message = ""
        if not message:
            _, message = retrieve_message_from_step_md(repo)
        if not message:
            readme_step, message = retrieve_message_from_commit(repo, step, 'main')
            if readme_step != step:
                warning(f"!!! {step} does not match {readme_step} - using {message}")
        # save message for next time
        # in repo this time
        step_md = Path("step.md")
        with step_md.open('w') as f:
            f.write(f"# {message}\n")
        completed = shell(f"git add step.md")


        completed = shell(f"git add {files_str}")
        completed = shell(f"git commit -m 'step {step} - {message}'")
        for file in files_list:
            to_remove = repo / file
            if to_remove.exists():
                debug(f"removing {to_remove}")
                to_remove.unlink()
                completed = shell(f"git rm {to_remove}")
            else:
                warning(f"!!! {to_remove} does not exist")

    # cleanup
    completed = shell(f"git reset --hard")
    # display current branches as we have switched to the new one
    completed = shell(f"git branch")

    return 0



def tofolders(git_repo: Path, output_root: Path) -> list[Path]:
    """
    given a git repo, will extract all suitable commits under the .steps folder
    this directory gets first deleted/re-created
    """
    if not (git_repo.exists() and git_repo.is_dir() and (git_repo / '.git').is_dir()):
        warning(f"!!! {git_repo} is not a valid directory")
        return None
    if output_root.is_dir():
        warning(f"!!! {output_root} already exists, deleting it")
        shell(f"rm -rf {output_root}")
    elif output_root.exists():
        warning(f"!!! {output_root} is not a directory")
        return None
    shell(f"mkdir {output_root}")

    def git_shell(git_command):
        command = f"git -C {git_repo} {git_command}"
        debug(command)
        return shell_capture(command)

    folders = []
    commit = git_shell(f"log --pretty='%h' -n 1")
    while True:
        logline = git_shell(f"log --pretty='%s' -n 1 {commit}")
        if match := COMMIT_MATCHER.match(logline):
            step = match.group("step")
            message = match.group("message")
            folder = output_root / step
            folders.append(folder)
            folder.mkdir()
            info(f"populating {folder.name}")
            command = f"git -C {git_repo} archive {commit} | tar -C {folder} -xf -"
            shell(command)
            step_md = folder / "step.md"
            if not step_md.exists():
                with step_md.open('w') as f:
                    f.write(f"# {message}\n")
        parent = git_shell(f"log --pretty='%p' -n 1 {commit}")
        if not parent or parent == commit:
            break
        commit = parent
    # return them in the order that chain-dirs would expect, older first
    return folders[::-1]


@cli.command('tofolders',
             help="create a folder hierarchy from a git repository - it creates a fresh history as the provided branch")
@click.option('-o', '--output-folder', type=Path, default=Path("--none--"), help="output folder, defaults to .steps")
@click.argument('git_repo', type=Path)
def tofolders_cli(output_folder, git_repo: Path) -> ShellSuccess:
    """
    this rebuilds the folder hierarchy from a git repository
    """
    if output_folder == Path("--none--"):
        output_folder = git_repo / ".steps"
    folders = tofolders(git_repo, output_folder)
    return 0 if folders else 1



@cli.command('strip-docstring', help="remove docstring from python files")
@click.argument('files', type=Path, nargs=-1)
def strip_docstring_cli(files: list[Path]) -> ShellSuccess:
    """
    this removes the docstring from the python files
    """
    for file in files:
        if file.is_file():
            message = strip_docstring(file)
            info(f"removed docstring from {file} - message was {message}")
        else:
            warning(f"{file} is not a file")
    return 0



@cli.command('diff-branches', help="compare two branches")
@click.argument('repo', type=Path)
@click.argument('branch1', type=str)
@click.argument('branch2', type=str)
def diff_branches(repo: Path, branch1: str, branch2: str) -> ShellSuccess:
    """
    this compares two branches
    """
    chdir(repo)
    repo = Path(".")
    info(f"working in {repo.absolute()}")

    def scan_branch(branch: str):
        command = f"git log --pretty='%h %s' {branch}"
        completed = shell(command, capture_output=True)
        lines = completed.stdout.decode().split("\n")
        d = {}
        for line in lines:
            if match := HASH_COMMIT_MATCHER.match(line):
                hash = match.group("hash")
                step = match.group("step")
                message = match.group("message")
                d[step] = (hash, message)
        debug(d)
        return d


    d1, d2 = scan_branch(branch1), scan_branch(branch2)
    if len(d1) != len(d2):
        warning(f"!!! {branch1} and {branch2} have different number of steps")
    if d1.keys() != d2.keys():
        warning(f"!!! {branch1} and {branch2} have different steps")
        info(f"{d1.keys()=}")
        info(f"{d2.keys()=}")

    for (s1, (h1, m1)), (s2, (h2, m2)) in zip(d1.items(), d2.items()):
        has_changes = False
        if s1 != s2 or m1 != m2:
            has_changes = True
        command = f"git diff {h1} {h2}"
        output = shell(command, capture_output=True)
        if output.stdout:
            has_changes = True
        if has_changes:
            info(40*'-')
            info(f"{h1}: {s1} - {m1}")
            info(f"{h2}: {s2} - {m2}")
            info(command)
            print(output.stdout.decode())
            # for smooth mixing with stderr where the context 
            # (step, file, ..) is printed
            sys.stdout.flush()


if __name__ == '__main__':
    cli()
