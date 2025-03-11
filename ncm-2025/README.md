# NCM-2025-materials

Materials for the Cantera workshop held in conjunction with the 2025 US National Combustion Meeting.

## Working with Jupytext Markdown Notebooks

The notebooks in this directory use the Jupytext extension to enable storing Git-friendly Markdown files rather than `.ipynb` format files that tend to record a lot of spurious changes and create diffs that are hard to read.

When you first check out this repository, you can open these notebooks in Jupyter by right clicking in the Jupyter file browser and selecting `Open With -> Jupytext Notebook` from the context menu.
As you make changes, both the `.md` and paired `.ipynb` file will be updated. When you want to commit your changes, only the `.md` should be added.

To create a new paired notebook, create a notebook as usual in the `.ipynb` format. A paired `.md` file should be created automatically based on settings in `pyproject.toml`.

For more about using Jupytext, see <https://blog.jupyter.org/the-jupytext-menu-is-back-3e6212e8c090>.
