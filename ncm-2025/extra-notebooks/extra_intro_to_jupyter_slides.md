---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"editable": true, "slideshow": {"slide_type": ""}}

# Overview of Jupyter Notebooks and Python

+++

## Jupyter Notebooks

+++

The Jupyter Notebook is an interactive browser-based programming environment that allows users to mix prose explanations, equations, and code in the same document.

The basic element of a Notebook is a "Cell". Each cell has a type:

* Markdown: Used for text and equations
* Code: Used for executable code
* Raw: Used for input that should not be processed by the Notebook (typically something that will be passed to an output processor, e.g., LaTeX).

where the first two are most commonly used. This cell is a Markdown cell.

```{code-cell} ipython3
# This cell is a code cell
```

Each cell also has two modes:

* Command mode: Blue border, keyboard commands trigger environment shortcuts
* Edit mode: Green border, keyboard commands enter text into the cell

Cells can be switched from Edit to Command by pressing `Esc` and from Command to Edit by clicking or double-clicking or by pressing `Enter/Return`.

+++

Finally, each cell has three states:

* Unexecuted
* In-Progress
* Executed/Rendered

Cells can be moved from the first Unexecuted state into the In-Progress state by three keyboard shortcuts:

* `Shift+Enter`: Execute the cell and select the next cell, appending a cell if at the bottom of the Notebook
* `Control+Enter`: Execute the cell and leave it selected
* `Alt/Option + Enter`: Execute the cell and insert a cell immediately below

There are also several UI functions that serve the same purposes:

* The "Run" button in the top toolbar
* The various "Run" options in the "Cell" menu
* The "Restart & Run" option in the Kernel menu

When Markdown cells are executed, they are rendered from monospace text to formatted text. When code cells are executed, the code in the cell is sent to the kernel associated with the Notebook, which executes the contents and returns any results (output, etc.)

+++

### What is a kernel?

Jupyter Notebooks are a language-agnostic format. Code cells are executed by a process running on the server called the kernel. There are kernels developed for many languages with varying levels of support. Python, as the original kernel, enjoys the best support but other options include:

* Matlab/Octave
* R
* C++
* Julia

and [more](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels). Kernels store the state of the computation, so any variables defined in a cell can be used in any other cell.

This leads to one of the most confusing parts of Jupyter Notebooks - they are non-linear. Since the execution of any cell modifies the state of the kernel, it can be confusing to keep track of the state of a variable as you move around in the Notebook. For instance, executing a cell at the bottom of a Notebook that changes the value of a variable `a`, then moving to the top of the Notebook and running a cell that relies on `a` will work fine, but can lead to difficult to diagnose behavior. When in doubt, Restarting the kernel erases all of the stored state and let's you start from a fresh slate.

+++

## Python

+++

Python is a general-purpose scripting language that has become very popular in the last 5-10 years. There are a few reasons for this, but in my opinion the main ones are

* The syntax is relatively easy to read
  * No braces
  * No semicolons
  * Meaningful whitespace enforces consistency
* Interpreted language, so a short feedback loop for programming
* An easy-to-extend C-API that lets users write high-performance code with easy-to-use interfaces

The combination of these mean that it is relatively easy for new users to have access to powerful code quickly.

+++

### Brief Overview of Syntax

The mathematical operators in Python are similar to other programming languages:

* `+`: Addition
* `-`: Subtraction
* `*`: Multiplication
* `/`: Division
* `**`: Power

To print some output to the screen, use `print()`.

```{code-cell} ipython3
print(2 + 2)
print(2 - 2)
print(2 * 2)
print(2 / 2)
print(2**2)
```

Python has several very common types that you will encounter:

* Integers: `var = 1`
* Floats: `var = 1.0`
* Strings: `var = "string"` (Python strings can use single or double quotes with the same meaning)

Notice that variable assignment is done with the variable on the left and the value on the right of the `=` sign. Trying to use a variable before it is defined will result in a `NameError`:

```{code-cell} ipython3
var = "a"
print(var)

print(not_a_var)
```

Python also has a number of data structures that are very useful:

* Dictionary: `var = {"key": "value"}`
  * Dictionaries are mappings of keys to values. Keys can be any hashable type (strings, floats, integers, and more), while values can be any type at all
* List: `var = ["elem1", 2.0, 3]`
  * Lists are a sequence of values. The values can be of any type and do not have to all be the same type. Lists are **mutable**; we can add and remove items from lists.
* Tuple: `var = ("elem1", 2.0, 3)`
  * Tuples are also a sequence of values, and like lists, the values can be of any type and do not all have to be the same type. The difference from lists is that tuples are **immutable** - to add or remove elements, we have to create a new tuple
* Arrays
  * Python does not natively have an "array" type. One can use nested lists of lists, but these tend to be inefficient. Fortunately, there is a third-party library called NumPy that provides a high-performance array library based on a C-extension for Python. We'll see more about NumPy a bit later on.
  
In Python, sequences (lists, tuples, and strings) and arrays are indexed with square brackets, and the indexing starts with 0. This is notably different from Matlab, so be careful! You can get a range of elements from a sequence with a _slice_ using the colon.

You can get the length of a sequence with `len()`.

```{code-cell} ipython3
var = ["a", "b", "c", 3.0]
print(var[0])
print(var[-1])
print(8*"=")

print(var[1:2])
print(var[:3])
print(var[2:])
print(8*"=")

print(len(var))
```

In Python, whitespace is meaningful. This means that code structures such as loops and conditionals use the leading whitespace on a line to delimit the beginning and end of the block. Each level of indentation is always 4 spaces (never tabs!). For instance:

```{code-cell} ipython3
var = "a"
if var == "a":
    print("Found a!")

for i in range(3):
    print(i)
print("The End")
```

In Python, the `#` symbol is used to create a comment in the code. (In a Jupyter Notebook, the `#` in a Markdown cell creates a header HTML element.)

```{code-cell} ipython3
# This is a comment in a code cell
```

# This is a header in a Markdown Cell

+++

---

The last stop on our tour of Python is importing. Python includes a fairly large standard library and people have also developed a huge number of libraries tha can be downloaded from the Python Package Index (PyPI, also called the cheese shop). To be able to use this code in a particular file or interpreter session, the library must be `import`ed. The `import` statement finds the requested library and allows you to access the functions in that library. Python also allows you to define aliases for a library so you don't have to type a long name over and over again.

```{code-cell} ipython3
import this
```

```{code-cell} ipython3
import antigravity
```

```{code-cell} ipython3
import sys
print(sys.version)
print(8*"=")

import cantera as ct
print(f"The version of Cantera is {ct.__version__}")
```

Note that we use the `.` (dot) notation for access in the imported modules' variables and functions. This is common in Python; essentially, the dot in `a.b` means **from within the object `a`, get (or set) the value of the attribute `b`**.

+++

### Python 2 or 3?

Python 3. No question. Official Python 2 support will end in on Jan. 1, 2020. Most scientific Python projects are dropping legacy Python support, including Cantera—2.4.0 is the last version of Cantera that will support legacy Python.

Note that on Linux and macOS, the default system version of Python accessed with the bare `python` executable is almost certainly Python 2 (I think the only exception is Arch Linux). Python 3 is accessed with the `python3` executable.

+++

# Do you want to know more?

+++

Check out the official Python Tutorial: https://docs.python.org/3/tutorial/ or search for Python tutorials, there are a bunch out there!
