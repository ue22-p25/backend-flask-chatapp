#!/usr/bin/env python
"""
given a list of folders - typically successive steps in building an app
produce a markdown fragment for insertion in a codehike input

it starts with comparing the first and second folder,
then the second and third, etc.

for each step it compares the files (under git) in the two folders
and produces a diff-like markdown fragment for each file
"""

import sys
import difflib
from pathlib import Path
from argparse import ArgumentParser
import subprocess as sp
from dataclasses import dataclass

import logging
logger = logging.getLogger('steps')
logging.basicConfig(level=logging.INFO)

(debug, info, warning, error) = logger.debug, logger.info, logger.warning, logger.error

import click

# when generating for scrolly coding, the output syntax is a little different
SCROLLY = False
# by default, we add a (sub)step for each file that is new or that has a change
# with this set to True, we only add a step if the change is described in a -step.md
ONLY_CHANGES_WITH_STEP = False


EXTENSIONS = {
    'requirements.txt': { 'lang': 'python', 'comment': lambda line: f"# {line}"},
    '.gitignore': { 'lang': 'python', 'comment': lambda line: f"# {line}"},
    '*.py' : { 'lang': 'python', 'comment': lambda line: f"# {line}"},
    '*.js' : { 'lang': 'js', 'comment': lambda line: f"// {line}"},
    '*.css': { 'lang': 'css', 'comment': lambda line: f"/* {line} */"},
    '*.html': { 'lang': 'html', 'comment': lambda line: f"<!-- {line} -->"},
    '*.text': { 'lang': 'text', 'comment': lambda line: f"{line}"},
    '*.html.j2': { 'lang': 'html', 'comment': lambda line: f"<!-- {line} -->"},
}


def defaults(path, filename, lang, comment):
    """
    Assign defaults for filename, lang, and comment based on path's name
    In general, all three are optional, however the caller may wish to specify any of these
    """
    for k, v in EXTENSIONS.items():
        if path.match(k):
            def_lang = v['lang']
            def_comment = v['comment']
            break
    else:
        # no match, so use the default
        # which should probably be 'text'
        # but https://github.com/code-hike/codehike/issues/514
        def_lang = 'python'
        def_comment = lambda line: f"# {line}"
    def_filename = path.name
    if comment and isinstance(comment, str):
        comment_str = comment
        comment = lambda line: f"{comment_str} {line}"
    return filename or def_filename, lang or def_lang, comment or def_comment


# https://github.com/code-hike/codehike/issues/507#issuecomment-2821673210
# annotations need to be within comments
# so we need to avoid writing annotations in the middle of strings
# typically doctings and similar
# so the strategy is to group all the annotations *before*
# the body itself
class DiffWriter:

    @dataclass
    class Annotation:
        mode: str   # '+' or '-' or '@'
        start: int  # start of the annotation
        end: int    # end of the annotation


    def __init__(self, comment):
        self.comment = comment
        self.mode = ' '  # could be '+', '-', ' ', or '@'
        self.annotations = []
        self.lines = []
        self.lineno = 0
        # for the current stream of + or -
        self.start = 0

    def add_line(self, line, mode):
        self.lineno += 1
        match mode:
            case '@':
                self.annotations.append(self.Annotation(mode, self.lineno, self.lineno))
                self.lines.append("........")
            case '+' | '-':
                if self.mode == mode:
                    self.annotations[-1].end = self.lineno
                else:
                    self.annotations.append(self.Annotation(mode, self.lineno, self.lineno))
                self.lines.append(line)
            case ' ':
                self.lines.append(line)

        self.mode = mode


    def flush(self):
        # write annotations
        for annotation in self.annotations:
            mode = annotation.mode
            match mode:
                case '+' | '-':
                    print(self.comment(f"!diff({annotation.start}:{annotation.end}) {mode}"))
                case '@':
                    print(self.comment(f"!className({annotation.start}) separator"))
        for line in self.lines:
            print(line)


def onefile_cat(file1, *, filename=None, lang=None, comment=None, added=True):
    """
    Print the contents of a file as a triple-fenced code block.
    if added is True, print the added lines with a green + sign
    otherwise use a red - sign
    """
    path1 = Path(file1)
    if not path1.exists():
        error(f"File {path1} does not exist.")
        return
    # assign from args or compute defaults
    filename, lang, comment = defaults(path1, filename, lang, comment)
    sign = '+' if added else '-'
    diff_writer = DiffWriter(comment)
    if not SCROLLY:
        print(f"```{lang} {filename}")
    else:
        print(f"```{lang} ! {filename}")
    with path1.open() as f:
        for line in f:
            line = line.rstrip()
            diff_writer.add_line(line, sign)
    diff_writer.flush()
    print("```")
    print()


def onefile_diff(file1, file2, *, filename=None, lang=None, comment=None):
    """
    Compare two files and print the differences as one triple-fenced code block.
    """
    path1, path2 = Path(file1), Path(file2)
    for path in [path1, path2]:
        if not path.exists():
            error(f"File {path} does not exist.")
            return
    # assign from args or compute defaults
    filename, lang, comment = defaults(path1, filename, lang, comment)

    lines1, lines2 = path1.read_text().splitlines(), path2.read_text().splitlines()
    if not SCROLLY:
        print(f"```{lang} {filename}")
    else:
        print(f"```{lang} ! {filename}")
    diff_writer = DiffWriter(comment)
    for line in difflib.unified_diff(lines1, lines2, str(file1), str(file2)):
        if line.startswith('---') or line.startswith('+++') or not line.strip():
            continue
        if line.startswith('@@'):
            diff_writer.add_line(line, '@')
            continue
        start, end = line[:1], line[1:]
        if start == ' ':
            diff_writer.add_line(line[1:], ' ')
            continue
        if start in ['-', '+']:
            diff_writer.add_line(end, start)
    diff_writer.flush()
    print("```")
    print()


def files_equal(file1, file2):
    """
    Check if two files are equal.
    """
    path1, path2 = Path(file1), Path(file2)
    if not path1.exists() or not path2.exists():
        return False
    return path1.read_text() == path2.read_text()


def onedir_diff(dir1, dir2, only_git):
    """
    compare two folders
    - files that appear in both: use onefile_diff
    - new files i.e. that appear in dir2 but not dir1:
      print a simple code block with the new one
    - deleted files: just mention them as deleted
    """
    path1, path2 = Path(dir1), Path(dir2)
    for path in [path1, path2]:
        if not path.exists():
            error(f"Directory {path} does not exist.")
            return
    d1, d2 = path1.name, path2.name
    # consider only files under git
    if only_git:
        sp1 = sp.run(['git', 'ls-files'], cwd=path1, capture_output=True)
        sp2 = sp.run(['git', 'ls-files'], cwd=path2, capture_output=True)
    else:
        sp1 = sp.run(['find', '.', '-type', 'f'], cwd=path1, capture_output=True)
        sp2 = sp.run(['find', '.', '-type', 'f'], cwd=path2, capture_output=True)
    files1 = sorted(set(sp1.stdout.decode().splitlines()))
    files2 = sorted(set(sp2.stdout.decode().splitlines()))

    global_step = dir2 / "step.md"
    if not global_step.exists():
        warning(f"File {global_step} does not exist!")
        dir_readme = "no dir readme !"
    else:
        with global_step.open() as f:
            # should contain '# the step readme'
            dir_readme = f.readline().strip()[2:]
            dir_readme = dir_readme.replace('<', '&lt;').replace('>', '&gt;')

    # ignore step.md in the list of files
    files1 = [f for f in files1 if not f.lower().endswith('step.md')]
    files2 = [f for f in files2 if not f.lower().endswith('step.md')]
    debug(f"files1: {files1}")
    debug(f"files2: {files2}")

    same_files =  sorted(set(files1) & set(files2))
    # discard files that are the same
    same_files = [f for f in same_files if not files_equal(path1 / f, path2 / f)]
    new_files = sorted(set(files2) - set(files1))
    deleted_files = sorted(set(files1) - set(files2))

    def handle_first_line(line, name, d1, d2, nth, total):
        if not line.startswith('## '):
            warning(f"README file {global_step} does not start with ##")
            title = "!!! MISSING TITLE in {d2}/{name} !!!"
        else:
            title = line[3:].strip()
            locator = f" ({nth}/{total})" if total != 1 else ""
        if SCROLLY:
            print(f"## !!steps {d2}{locator}: {dir_readme}")
        else:
            # the headers has been inserted already as a TableOfContentsItem
            pass
            # print(f"## step {d2}{locator}: {dir_readme}")

        if d1:
            print(f"### {d1} -> {d2} - changes in {name}")
        else:
            print(f"### {d2} : new file {name}")

        print(f"#### {title}")

    def has_step(path, *, new_dir):
        return (path.parent / (path.name + '-step.md')).exists()

    def handle_step(path, *, new_dir, nth, total=None, old_dir=None):
        """
        d1=None mean it's a new file in d2
        """
        file_step = path.parent / (path.name + '-step.md')
        if file_step.exists():
            with file_step.open() as f:
                for lineno, line in enumerate(f, 1):
                    if lineno == 1:
                        handle_first_line(line, path.name, old_dir, new_dir, nth, total)
                    else:
                        print(line, end="")
                if not line.endswith('\n'):
                    print()
        else:
            warning(f"File {file_step} does not exist!")
            warning(f"output likely broken !!!")

    def heading_details(file, nth, total):
        nth_verbose = f" - {nth}/{total}" if total != 1 else " - "
        topic = f"step {d2}{nth_verbose} {dir_readme}"
        if nth == 1:
            label = f"{d2} {dir_readme}"
        else:
            label = f"{d2}{nth_verbose}"
        return topic, label


    # open the possibility to specify an order
    def handle_same_file(file, nth, total):
        info(f"changes in file: {file}")
        topic, label = heading_details(file, nth, total)
        if not SCROLLY:
            print(f"<TableOfContentsItem topic='{topic}' label='{label}'>")
        handle_step(path2 / file, old_dir=d1, new_dir=d2, nth=nth, total=total)
        onefile_diff(path1 / file, path2 / file)
        if not SCROLLY:
            print(f"</TableOfContentsItem>")


    def handle_new_file(file, nth, total):
        info(f"new file: {file2}")
        topic, label = heading_details(file, nth, total)

        if not SCROLLY:
            print(f"<TableOfContentsItem topic='{topic}' label='{label}'>")
        handle_step(path2 / file, new_dir=d2, nth=nth, total=total)
        onefile_cat(path2 / file2, added=True)
        if not SCROLLY:
            print(f"</TableOfContentsItem>")

    if ONLY_CHANGES_WITH_STEP:
        same_files = [f for f in same_files if has_step(path2 / f, new_dir=d2)]
        new_files = [f for f in new_files if has_step(path2 / f, new_dir=d2)]
        debug(f"same_files (kept only with -step.md): {same_files}")
        debug(f"new_files (kept only with -step.md): {new_files}")

    total_changes = len(same_files) + len(new_files) + len(deleted_files)

    nth = 1
    for file in same_files:
        handle_same_file(file, nth, total_changes)
        nth += 1
    for file2 in new_files:
        handle_new_file(file2, nth, total_changes)
        nth += 1

    for file1 in deleted_files:
        warning(f"deleted file : {file1}")
        print(f"## {nth}/{total_changes} deleted in {d2}: {file1}")
        nth += 1

def chaindirs(paths, only_git):
    """
    accepts a sequence of at least 2 paths
    then will run onefile_diff on each pair of successive paths
    """
    for a, b in zip(paths, paths[1:]):
        info(f"==== comparing {a.name} and {b.name}")
        onedir_diff(a, b, only_git)

# using click to expose one command per function

@click.group(chain=True, help=sys.modules[__name__].__doc__)
@click.option("--debug", is_flag=True, help="enable debug output")
@click.option("--quiet", is_flag=True, help="enable debug output")
def cli(debug, quiet):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    if quiet:
        logging.getLogger().setLevel(logging.WARNING)


@cli.command('diff-files', help="write out diff between two files")
@click.option('-f', '--filename', type=str, help='Filename for the output')
@click.option('-l', '--lang', type=str, default='python', help='Language for syntax highlighting')
@click.option('-c', '--comment', type=str, default=None, help='Comment character for the language')
@click.argument('file1', type=Path)
@click.argument('file2', type=Path)
def onefile_cli(filename, lang, comment, file1, file2):
    onefile_diff(
        file1, file2, filename=filename, lang=lang, comment=comment,
    )


@cli.command('diff-dirs', help="write out diff between two directories")
@click.argument('dir1', type=Path)
@click.argument('dir2', type=Path)
def onedir_cli(dir1, dir2):
    onedir_diff(dir1, dir2)


@cli.command('chain-dirs', help="write out diff between a succession of directories")
@click.option('-s', '--scrolly', is_flag=True, help='Use scrolly mode')
@click.option('-a', '--all-files', is_flag=True, help="consider all files, not just the ones under git")
@click.option('-o', '--only-changes-with-step', is_flag=True, help="only show changes with a step.md file")
@click.argument('dirs', type=Path, nargs=-1)
def chaindirs_cli(scrolly, all_files, only_changes_with_step, dirs):
    if len(dirs) < 2:
        error("At least two directories are required for comparison.")
        return
    global SCROLLY
    SCROLLY = scrolly
    global ONLY_CHANGES_WITH_STEP
    ONLY_CHANGES_WITH_STEP = only_changes_with_step

    chaindirs(dirs, only_git=not all_files)


if __name__ == "__main__":
    cli()
