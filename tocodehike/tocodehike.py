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

EXTENSIONS = {
    '.py' : { 'lang': 'python', 'comment': lambda line: f"# {line}"},
    '.js' : { 'lang': 'js', 'comment': lambda line: f"// {line}"},
    '.css': { 'lang': 'css', 'comment': lambda line: f"/* {line} */"},
    '.html': { 'lang': 'html', 'comment': lambda line: f"<!-- {line} -->"},
    '.text': { 'lang': 'text', 'comment': lambda line: f"{line}"},
}

def add_lang_index():
    global EXTENSIONS
    for ext, info in list(EXTENSIONS.items()):
        lang = info['lang']
        if lang not in EXTENSIONS:
            EXTENSIONS[lang] = info

add_lang_index()


def md_title(title, level=2):
    """
    output a markdown title.
    """
    print(f"{level*'#'} {title}\n")


def defaults(path, filename, lang, comment):
    """
    Assign defaults for filename, lang, and comment based on the file extension.
    """
    if filename is None:
        filename = path.name
    suffix = Path(filename).suffix
    extension = EXTENSIONS.get(suffix, {}) or EXTENSIONS.get(lang, {})
    lang = lang or extension.get('lang', 'text')
    if comment and isinstance(comment, str):
        comment_str = comment
        comment = lambda line: f"{comment_str} {line}"
    comment = comment or extension.get('comment', lambda line: line)
    return filename, lang, comment


def onefile_cat(file1, *, filename=None, lang=None, comment=None, added=True):
    """
    Print the contents of a file as a triple-fenced code block.
    if added is True, print the added lines with a green + sign
    otherwise use a red - sign
    """
    path1 = Path(file1)
    if not path1.exists():
        print(f"File {path1} does not exist.", sys.stderr)
        return
    # assign from args or compute defaults
    filename, lang, comment = defaults(path1, filename, lang, comment)
    sign = '+' if added else '-'
    print(f"```{lang} {filename}")
    with path1.open() as f:
        for line in f:
            print(comment("!diff {sign}"))
            print(line)
    print("```")
    print()


def onefile_diff(file1, file2, *, filename=None, lang=None, comment=None):
    """
    Compare two files and print the differences as one triple-fenced code block.
    """
    path1, path2 = Path(file1), Path(file2)
    for path in [path1, path2]:
        if not path.exists():
            print(f"File {path} does not exist.", sys.stderr)
            return
    # assign from args or compute defaults
    filename, lang, comment = defaults(path1, filename, lang, comment)

    lines1, lines2 = path1.read_text().splitlines(), path2.read_text().splitlines()
    print(f"```{lang} {filename}")
    for line in difflib.ndiff(lines1, lines2):
        start, end = line[:2], line[2:]
        match start:
            case '- ' | '+ ':
                print(comment(f"!diff {start.rstrip()}"))
                print(end)
            case '  ':
                print(end)
    print("```")
    print()


def onedir_diff(dir1, dir2):
    """
    compare two folders
    - files that appear in both: use onefile_diff
    - files that appear in one but not the other: print a simple code block
    """
    path1, path2 = Path(dir1), Path(dir2)
    for path in [path1, path2]:
        if not path.exists():
            print(f"Directory {path} does not exist.", sys.stderr)
            return
    # consider only files under git
    sp1 = sp.run(['git', 'ls-files'], cwd=path1, capture_output=True)
    files1 = sorted(set(sp1.stdout.decode().splitlines()))
    sp2 = sp.run(['git', 'ls-files'], cwd=path2, capture_output=True)
    files2 = sorted(set(sp2.stdout.decode().splitlines()))

    md_title(f"changes from {path1} to {path2}")

    file1 = file2 = None
    while files1 and files2:
        file1, file2 = files1[0], files2[0]
        if file1 == file2:
            md_title(f"common file: {file1}", level=3)
            onefile_diff(path1 / file1, path2 / file2)
            files1.pop(0)
            files2.pop(0)
        elif file1 < file2:
            md_title(f"deleted file: {file1}", level=3)
            # on second thought, no need to show the old file if it gets deleted
            # onefile_cat(path1 / file1, added=False)
            files1.pop(0)
        else:
            md_title(f"new file: {file2}", level=3)
            onefile_cat(path2 / file2, added=True)
            files2.pop(0)


def dirchain(paths):
    """
    accepts a sequence of at least 2 paths
    then will run onefile_diff on each pair of successive paths
    """
    for a, b in zip(paths, paths[1:]):
        print(f"comparing {a} and {b}", file=sys.stderr)
        onedir_diff(a, b)


# xxx use click

def onefile_cli():
    parser = ArgumentParser(description="Compare two files and print the differences.")
    parser.add_argument('file1', type=Path, help='First file to compare')
    parser.add_argument('file2', type=Path, help='Second file to compare')
    parser.add_argument('-l', '--lang', type=str, default='python', help='Language for syntax highlighting')
    parser.add_argument('-c', '--comment', type=str, default=None, help='Comment character for the language')
    parser.add_argument('-f', '--filename', type=str, help='Filename for the output')

    args = parser.parse_args()

    onefile_diff(
        args.file1, args.file2,
        lang=args.lang,
        comment=args.comment,
        filename=args.filename)


def onedir_cli():
    parser = ArgumentParser(description="Compare two directories and print the differences.")
    parser.add_argument('dir1', type=Path, help='First directory to compare')
    parser.add_argument('dir2', type=Path, help='Second directory to compare')

    args = parser.parse_args()

    onedir_diff(args.dir1, args.dir2)


def dirchain_cli():
    parser = ArgumentParser(description="Compare two directories and print the differences.")
    parser.add_argument('dirs', type=Path, nargs='+', help='Directories to compare')
    args = parser.parse_args()

    if len(args.dirs) < 2:
        print("At least two directories are required for comparison.")
        return

    dirchain(args.dirs)


def main():
    dirchain_cli()


if __name__ == "__main__":
    main()
