#!/usr/bin/env python

from argparse import ArgumentParser
from pathlib import Path

from jinja2 import Environment

def handle_folder(folder):
    """
    in provided folder:
    - looks for a file named AUTO
    - looks for all files named *.j2
    - and in each replace {{AUTO}} with the content of AUTO
    """
    auto_file = folder / 'AUTO'
    if not auto_file.exists():
        print(f"File AUTO not found in {folder}")
        return
    with auto_file.open() as file_in:
        AUTO = file_in.read()
    for template_path in folder.glob('*.j2'):
        environment = Environment()
        with template_path.open() as file_in:
            template = environment.from_string(file_in.read())
        output = template_path.parent / template_path.stem
        with output.open('w') as file_out:
            rendered = template.render(AUTO=AUTO)
            file_out.write(rendered)
        print(f"{output} (over)written")


def main():
    parser = ArgumentParser()
    parser.add_argument('folders', type=Path, nargs='+')
    args = parser.parse_args()

    for folder in args.folders:
        handle_folder(folder)


if __name__ == "__main__":
    main()
