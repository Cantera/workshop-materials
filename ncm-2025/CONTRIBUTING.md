# NCM-2025-materials

Materials for the Cantera workshop held in conjunction with the 2025 US National Combustion Meeting.

## Working with Jupytext Markdown Notebooks

The notebooks in this directory use the Jupytext extension to enable storing markdown text within Git-friendly annotated Python `.py` files rather than within `.ipynb` format files that tend to record a lot of spurious changes and create diffs that are hard to read.

For more about using Jupytext, see <https://blog.jupyter.org/the-jupytext-menu-is-back-3e6212e8c090>.

### Jupyter Lab

When you first check out this repository, you can open these notebooks in Jupyter by right clicking in the Jupyter file browser and selecting `Open With -> Jupytext Notebook` from the context menu.
As you make changes, both the `.py` and paired `.ipynb` file will be updated. When you want to commit your changes, only the `.py` should be added.

To create a new paired notebook, create a notebook as usual in the `.ipynb` format. A paired `.py` file should be created automatically based on settings in `pyproject.toml`.

### VS Code

Make sure that you install the _Python_ and _Jupyter_ extensions.

Once extensions are installed, you can execute notebooks in VS Code by opening the regular Python files, where the percent `# %%` annotation breaks the code into code cells. You can step through the notebook by hitting `Shift+Return`, which opens an interactive window displaying results. You can also right click on a file in the file browser and select `Run Current File in Interactive Window`, which will execute the entire script, and render both markdown and code output.

In order to display expanded code blocks in interactive windows, open `Preferences: Open Settings (UI)`, select the _User_ tab, navigate to `Features` and `Notebook`, and switch `Interactive Window: Collapse Cell Input Code` to `never`.

### Spyder

Similar to VS Code, the Spyder IDE allows for stepping through a `.py` file using `Shift+Return`. Markdown output is, however, not rendered.
