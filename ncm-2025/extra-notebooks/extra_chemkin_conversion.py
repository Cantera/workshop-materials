# %% [markdown]
# ## Converting from Chemkin

# %% [markdown]
# Cantera comes with a script to convert CHEMKIN input files to the YAML format. This script is called `ck2yaml`. There are three ways to call `ck2yaml`:
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
# 3. If you are already running a Python interpreter (`python`, IPython, Jupyter Notebook, etc.) you can directly call the `convert_mech` function from the `ck2yaml` module
#
#    ```python
#    from cantera.ck2yaml import convert_mech
#    convert_mech?
#    ```

# %%
from cantera.ck2yaml import convert_mech
# convert_mech?

# %% [markdown]
# There is one mandatory argument to `convert_mech` (and the command line equivalents):
#
# - `input_file`: The CHEMKIN input file that contains at least an `ELEMENTS`, `SPECIES`, and `REACTIONS` section, and optionally contains a `THERMO` or `TRANSPORT` section
#
# There are seven other optional arguments to `convert_mech` (and the command line equivalents):
#
# - `thermo_file`: A CHEMKIN-formatted file with thermodynamics data for the species present in the `input_file`. Must be passed if the thermodynamics data is not present in the `input_file`
# - `transport_file`: A CHEMKIN-formatted file with transport data for the species present in the `input_file`
# - `surface_file`: A Surface CHEMKIN-formatted input file with surface reactions
# - `phase_name`: The name of the phase that should be created in the resulting CTI file
# - `out_name`: The filename of the CTI output file
# - `quiet`: Reduce the output from the conversion
# - `permissive`: Convert some ambiguous input conditions from errors to warnings
#
# One of the most common problems that users encounter is converting CHEMKIN format input files to Cantera YAML format. Unfortunately, the CHEMKIN interpreter for these files is not very strict about complying with its own standard, so files that appear to work just fine in CHEMKIN require some massaging to work with Cantera. Let's look at one example using the `convert_mech` function.

# %%
convert_mech(
    input_file='input-files/mech_debug/mech.txt',
    thermo_file='input-files/mech_debug/thermo.txt',
    transport_file='input-files/mech_debug/tran.txt',
    out_name='input-files/mech_debug/mech.yaml',
);

# %% [markdown]
# The key error message here is:
#
# ```
# WARNING:root:
# ERROR: Unable to parse 'input-files/mech_debug/mech.txt' near line 73:
# ...
# InputError: Unrecognized token on REACTIONS line, 'BASE'
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
# The error is occuring because Cantera doesn't know how to interpret the `BASE M=N2` portion of that line. It appears to be a comment from the mechanism author about the default identity of the bath gas, so we can probably safely delete that portion of the line. Let's do that and save the file as `mech_fixed.txt` and try the conversion again:

# %%
convert_mech(
    input_file='input-files/mech_debug/mech_fixed.txt',
    thermo_file='input-files/mech_debug/thermo.txt',
    transport_file='input-files/mech_debug/tran.txt',
    out_name='input-files/mech_debug/mech.cti',
);

# %% [markdown]
# There are a few things to parse out of this error message. First, there are a number of warnings about species whose thermodynamics properties are provided in the `thermo.txt` file but are not declared as valid species in the `SPECIES` secton of the `mech_fixed.txt` file:
#
# ```
# INFO:root:Skipping unexpected species "C3H4CY" while reading thermodynamics entry.
# INFO:root:Skipping unexpected species "C4H5" while reading thermodynamics entry.
# INFO:root:Skipping unexpected species "CH3NO3" while reading thermodynamics entry.
# INFO:root:Skipping unexpected species "CH2NO3" while reading thermodynamics entry.
# INFO:root:Skipping unexpected species "HCCOH" while reading thermodynamics entry.
# INFO:root:Skipping unexpected species "N2O5" while reading thermodynamics entry.
# ```
#
# We can safely ignore these warnings because the mechanism file won't use these species data anyways. The next line starts the actual error that caused the conversion to fail:
#
# ```
# INFO:root:Error while reading thermo entry starting on line 526:
# """
# TC4H7             A 8/83C   4H	 7    0    0G   300.     3000.	  1500.        1
#  0.4219753E 01  0.2882451E-01 -0.1399213E-04  0.3340718E-08 -0.3226427E-12     2
#  0.1266295E 05  0.3253111E 01 -0.2152314E+01  0.5547424E-01 -0.6226715E-04     3
#  0.4593056E-07 -0.1492297E-10  0.1407443E 05  0.3421103E 02  0.1543086E+05     4
# """
# WARNING:root:
# ERROR: Unable to parse 'input-files/mech_debug/thermo.txt' near line 526:
# ...
# ValueError: could not convert string to float: 'E-08 -0.32'
# ```
#
# This one is really tricky to figure out. The error here is because of some bad input on the first line of the thermo section (the `ValueError` is a bit of a red herring). The CHEMKIN/NASA fixed-format specification says that there should be spaces between each of the entries on the first line, but this input file includes a tab character on that line rather than spaces. We can see this by inspecting the file in an editor that shows whitespace characters.
#
# Once that line is fixed, we can try the conversion again:

# %%
convert_mech(
    input_file='input-files/mech_debug/mech_fixed.txt',
    thermo_file='input-files/mech_debug/thermo_fixed.txt',
    transport_file='input-files/mech_debug/tran.txt',
    out_name='input-files/mech_debug/mech.yaml',
);

# %% [markdown]
# In this output, we can see the same warnings about undeclared species and then the error output:
#
# ```
# InputError: Ignoring duplicate transport data for species "NCN" on line 152 of "input-files/mech_debug/tran.txt".
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
# Let's supply the `permissive` option to the converter and see what happens:

# %%
convert_mech(
    input_file='input-files/mech_debug/mech_fixed.txt',
    thermo_file='input-files/mech_debug/thermo_fixed.txt',
    transport_file='input-files/mech_debug/tran.txt',
    out_name='input-files/mech_debug/mech.yaml',
    permissive=True,
);

# %% [markdown]
# And finally, we have successfully converted the file.
#
# We have compiled a list of the most common errors in CHEMKIN format input files, which you can find in our documentation: https://cantera.org/tutorials/ck2cti-tutorial.html#debugging-common-errors-in-ck-files
