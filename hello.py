import argparse
import datetime
import os
import pathlib
import subprocess
import tempfile

import editdistance
from prompt_toolkit import application
from prompt_toolkit import layout
from prompt_toolkit.layout import containers
import ptterm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--top-margin", type=int, default=0)
    args = parser.parse_args()

    content_path = pathlib.Path(args.file)
    content = content_path.read_text()

    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tempdir:
        def done():
            es.exit()

        tempdir = pathlib.Path(tempdir)
        edited_file = tempdir / content_path.name

        editor_command = ["bash", "-c", f"$EDITOR {edited_file}"]

        editor = ptterm.Terminal(done_callback=done, command=editor_command)
        text = layout.Window(containers.FormattedTextControl("\n" * args.top_margin + content), dont_extend_width=True)

        es = application.Application(layout=layout.Layout(layout.VSplit([editor, text])), full_screen=True)

        start = datetime.datetime.now()
        es.run()

        total_seconds = (datetime.datetime.now() - start).total_seconds()
        words = len(content.split())

        print("Total seconds", total_seconds)
        print("Edit distance", editdistance.eval(content, edited_file.read_text()))
        print('"Words"', words)
        print('"Words"/minute', words / (total_seconds / 60))

        subprocess.run(["diff", content_path, edited_file])


if __name__ == '__main__':
    main()
