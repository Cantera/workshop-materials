# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Converting from Chemkin

# %% [markdown]
# Cantera comes with a script to convert CHEMKIN input files to the YAML format. This script is called `ck2yaml`. There are two ways to call `ck2yaml`:
#
# 1. Directly from the command line or terminal prompt
#
#    ```
#    ck2yaml --help
#    ```
#
#    This assumes that `ck2yaml` is installed somewhere on your `PATH`.
#
# 2. If you have multiple versions of Cantera installed, or `ck2yaml` is not on your `PATH`, you can also have Python find the `ck2yaml` module and run that:
#
#    ```
#    python -m cantera.ck2yaml --help
#    ```
#

# %%
# !ck2yaml --help

# %% [markdown]
# There is one mandatory argument to `ck2yaml`:
#
# - `--input`: The CHEMKIN input file that contains at least an `ELEMENTS`, `SPECIES`, and `REACTIONS` section, and optionally contains a `THERMO` or `TRANSPORT` section
#
# There are several other optional arguments:
#
# - `--thermo`: A CHEMKIN-formatted file with thermodynamics data for the species present in the `input` file. Must be provided if the thermodynamics data is not present in the `input` file
# - `--transport`: A CHEMKIN-formatted file with transport data for the species present in the `inputFile`
# - `--surface`: A Surface CHEMKIN-formatted input file with surface reactions
# - `--name`: The name of the phase that should be created in the resulting YAML file
# - `--output`: The filename of the YAML output file
# - `--quiet`: Reduce the output from the conversion
# - `--permissive`: Convert some ambiguous input conditions from errors to warnings
#
# One of the most common problems that users encounter is converting CHEMKIN format input files to Cantera YAML format. Unfortunately, the CHEMKIN interpreter for these files is not very strict about complying with its own standard, so files that appear to work just fine in CHEMKIN require some massaging to work with Cantera. Let's look at one example using `ck2yaml`:

# %%
# !ck2yaml --input=../inputs/mech_debug/mech.txt --thermo=../inputs/mech_debug/thermo.txt --transport=../inputs/mech_debug/tran.txt --output=mech.yaml

# %% [markdown]
# ## Fixing REACTIONS error:
#
# Cantera reports several errors here. The first two are related to the declaration of the `REACTIONS` section:
#
# ```
# *******************************************************************************
# Error while reading section in mech.txt starting on line 73:
# """
# REACTIONS          BASE M=N2
# """
# Unrecognized token 'BASE' on REACTIONS line
# *******************************************************************************
# Error while reading section in mech.txt starting on line 73:
# """
# REACTIONS          BASE M=N2
# """
# Unrecognized token 'M=N2' on REACTIONS line
# *******************************************************************************
# ```
#
# Looking at the input file at line 73, we find the end of the `SPECIES` section and the start of the `REACTIONS` section:
#
# ```text
# 70  C6H5      ! phenyl        
# 71  AR        N2
# 72  END
# 73  REACTIONS          BASE M=N2
# ```
#
# The error is occuring because Cantera doesn't know how to interpret the `BASE M=N2` portion of that line. It appears to be a comment from the mechanism author about the default identity of the bath gas, so we can probably safely delete that portion of the line. Let's do that and save the file as `mech_fixed.txt`.

# %% [markdown]
#

# %% [markdown]
# ## Fixing the thermo error:
# ```
# *******************************************************************************
# Unparsable lines while reading thermo data in thermo.txt starting on line 523:
# """
# TC4H7             A 8/83C   4H	 7    0    0G   300.     3000.	  1500.        1
#  0.4219753E 01  0.2882451E-01 -0.1399213E-04  0.3340718E-08 -0.3226427E-12     2
#  0.1266295E 05  0.3253111E 01 -0.2152314E+01  0.5547424E-01 -0.6226715E-04     3
#  0.4593056E-07 -0.1492297E-10  0.1407443E 05  0.3421103E 02  0.1543086E+05     4
# """
# Lines could not be parsed as a NASA7 entry. Run ck2yaml again with the
# '--permissive' option to continue without parsing these lines.
# *******************************************************************************
# ```
#
# This one is really tricky to figure out. The error here is because of some bad input on the first line of the thermo section. The CHEMKIN/NASA fixed-format specification says that each value should be at a specific character position in each line, but this input file includes multiple tab characters on the first line rather than spaces (after `4H` and `3000.`). We can see this by inspecting the file in an editor that shows whitespace characters.
#
# We can replace these tabs with the correct number of spaces and then save the input file as `thermo_fixed.txt` before re-running the conversion.
#

# %% [markdown]
# ## Fixing the transport error:
#
# ```
# *******************************************************************************
# Error while reading transport data in tran.txt starting on line 152:
# """
# NCN                1   232.400     3.828     0.000     0.000     1.000 ! OIS
# """
# Duplicate transport data for species 'NCN'. Run ck2yaml again with the
# '--permissive' option to ignore this redundant entry.
# *******************************************************************************
# ```
#
# This is a case where the input file is valid syntactically, but the possible output conditions are ambiguous. In the transport file, there are two definitions of the properties for the species `NCN`:
#
# ```
# 108  NCN                1   232.400     3.828     0.000     0.000     1.000 !=CNN
# ...
# 152  NCN                1   232.400     3.828     0.000     0.000     1.000 ! OIS
# ```
#
# Fortunately, both of these sets of properties are identical, so it doesn't matter which one is picked. In this case, you can use the `permissive` option to the converter to allow this error to pass with just a warning, and the converter will automatically use the first declaration of the species. This is also a common problem with thermodynamics input files.
#
# If the inputs were different, it would be up to you to choose which input is more correct and comment out or delete the other one.
#
#

# %% [markdown]
# ## Re-running the conversion with corrected input files
#
# Let's use the fixed `mech.txt` and `thermo.txt` files, and supply the `permissive` option to ignore the issue with the transport data:

# %%
# !ck2yaml --input=../inputs/mech_debug/mech_fixed.txt --thermo=../inputs/mech_debug/thermo_fixed.txt --transport=../inputs/mech_debug/tran.txt --output=mech.yaml --permissive

# %% [markdown]
# And finally, we have successfully converted the file.
#
# However, there are numerous warnings about discontinuous thermo data, which are suspicious and may warrant investigation.
#
# We have compiled a list of the most common errors in CHEMKIN format input files, which you can find in our documentation: https://cantera.org/stable/userguide/ck2yaml-tutorial.html#sec-debugging-chemkin

# %%
