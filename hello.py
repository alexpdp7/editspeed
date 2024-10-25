import argparse
import datetime
import os
import pathlib
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
        split = layout.Window(width=1, char="|", style="class:line")
        text = layout.Window(containers.FormattedTextControl("\n" * args.top_margin + content))

        es = application.Application(layout=layout.Layout(layout.VSplit([editor, split, text])), full_screen=True)

        start = datetime.datetime.now()
        es.run()
        print(datetime.datetime.now() - start, editdistance.eval(content, edited_file.read_text()))


if __name__ == '__main__':
    main()
