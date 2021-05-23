from pathlib import Path
from typing import Any, Dict, Tuple, TYPE_CHECKING

import nbformat
from nbconvert import NotebookExporter
from nbconvert.preprocessors import Preprocessor
from nbformat.v4 import new_code_cell, upgrade

if TYPE_CHECKING:
    from nbformat import NotebookNode  # noqa: F401 # typing only


class CleanTagReplacer(Preprocessor):
    """Replace cells tagged 'clean' with a dummy cell"""

    def preprocess(
            self, nb: "NotebookNode", resources: Dict[Any, Any]
    ) -> Tuple["NotebookNode", Dict[Any, Any]]:
        """Preprocess the entire notebook."""
        for i, cell in enumerate(nb.cells):
            if "tags" in cell.metadata and "clean" in cell.metadata["tags"]:
                nb.cells[i] = new_code_cell(source="# Write Python source code in this cell")

        return nb, resources


nb_exp = NotebookExporter(preprocessors=[CleanTagReplacer])

if __name__ == "__main__":
    HERE = Path(__file__).parent
    output_directory = HERE.joinpath("output")

    for notebook in HERE.glob("**/*.ipynb"):
        if "checkpoints" in str(notebook):
            continue
        print(notebook)
        output_notebook = notebook.with_stem(notebook.stem + "-clean").name
        nb = nbformat.read(notebook, as_version=4)
        nb_new = upgrade(nb)
        if nb_new is not None:
            nb = nb_new
        if "celltoolbar" in nb.metadata:
            del nb.metadata["celltoolbar"]

        clean_nb, _ = nb_exp.from_notebook_node(nb)
        nbformat.write(nbformat.reads(clean_nb, as_version=4), notebook) 
