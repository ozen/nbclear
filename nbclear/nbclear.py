import argparse
import datetime
import io
import os
import sys
from typing import Optional
from typing import Sequence

import nbformat
from traitlets.config import Config
from nbconvert.exporters import NotebookExporter
from nbconvert.writers import FilesWriter


def _open_notebook(filename):
    resources = {}
    resources["metadata"] = {}
    path, basename = os.path.split(filename)
    notebook_name = os.path.splitext(basename)[0]
    resources["metadata"]["name"] = notebook_name
    resources["metadata"]["path"] = path

    modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    # datetime.strftime date format for ipython
    if sys.platform == "win32":
        date_format = "%B %d, %Y"
    else:
        date_format = "%B %-d, %Y"
    resources["metadata"]["modified_date"] = modified_date.strftime(date_format)

    with io.open(filename, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    return nb, resources


def _clear_notebook(filename, exporter, writer):
    nb_in, resources_in = _open_notebook(filename)
    body, resources_out = exporter.from_notebook_node(nb_in, resources=resources_in)
    nb_out = nbformat.reads(body, as_version=4)
    if nb_in == nb_out:
        # no changes needed
        return False
    else:
        # backup the original notebook
        backup_filename = filename + "~"
        try:
            os.rename(filename, backup_filename)
        except Exception as e:
            print(f"Could not create backup for {os.path.basename(filename)}: {e}")
            return True

        # write the cleared notebook to the original path
        notebook_name, _ = os.path.splitext(filename)
        writer.write(body, resources_out, notebook_name=notebook_name)
        print(f"Cleared {os.path.basename(filename)}, backed up the original to {os.path.basename(backup_filename)}")
        return True


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    c = Config()
    c.NotebookExporter.preprocessors = [
        "nbconvert.preprocessors.ClearOutputPreprocessor"
    ]
    exporter = NotebookExporter(config=c)
    writer = FilesWriter()

    ret = 0
    for filename in args.filenames:
        filename = os.path.abspath(filename)
        _, extension = os.path.splitext(filename.lower())
        if extension == ".ipynb":
            ret |= _clear_notebook(filename, exporter, writer)
    return ret


if __name__ == "__main__":
    raise SystemExit(main())
