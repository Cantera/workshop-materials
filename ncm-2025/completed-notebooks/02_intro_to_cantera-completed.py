# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Cantera Tutorial: Python

# %% [markdown]
# ### Getting Started

# %% [markdown]
# Let's get started with Cantera by importing the Cantera and NumPy libraries. We can also print the version of Cantera that we're using with the `__version__` attribute from the `cantera` module, typically aliased as `ct`.

# %%
import cantera as ct
import numpy as np

print(f"Using Cantera version {ct.__version__}")

# %% [markdown]
# When using Cantera, the first thing you usually need is an object representing some phase of matter. Here, we'll create a gas mixture:

# %%
gas1 = ct.Solution('gri30.yaml')

# %% [markdown]
# To view the state of the mixture, *call* the `gas1` object as if it were a function:

# %%
gas1()

# %% [markdown]
# What you have just done is created an object `gas1` that implements GRI-Mech 3.0, the 53-species, 325-reaction natural gas combustion mechanism developed by Gregory P. Smith, David M. Golden, Michael Frenklach, Nigel W. Moriarty, Boris Eiteneer, Mikhail Goldenberg, C. Thomas Bowman, Ronald K. Hanson, Soonho Song, William C. Gardiner, Jr., Vitali V. Lissianski, and Zhiwei Qin.  See the [GRI-Mech Home Page](http://combustion.berkeley.edu/gri-mech/) for more information.
#
# The `gas1` object has properties you would expect for a gas mixture: a temperature, a pressure, species mole and mass fractions, etc. As we will soon see, it has many more properties.
#
# The summary of the state of `gas1` that you found above shows that the new objects created from the `gri30.yaml` input file start out with a temperature of 300 K, a pressure of 1 atm, and have a composition that consists of only one species, in this case hydrogen. There is nothing special about H2—it just happens to be the first species listed in the input file defining GRI-Mech 3.0. In general, whichever species is listed first will initially have a mole fraction of 1.0, and all others will be zero.

# %% [markdown]
# ### Setting the State

# %% [markdown]
# The state of the object can easily be changed. For example:

# %%
gas1.TP = 1200, 101325

# %% [markdown]
# sets the temperature to 1200 K and the pressure to 101325 Pa (Cantera always uses SI units + kmol). After this statement, calling `gas1()` results in:

# %%
gas1()

# %% [markdown]
# Thermodynamics generally requires that *two* properties in addition to composition information be specified to fix the intensive state of a substance (or mixture). The state of the mixture can be set using several combinations of two properties. The following are all equivalent:

# %%
gas1.TP = 1200, 101325            # temperature, pressure
gas1.TD = 1200, 0.0204723         # temperature, density
gas1.HP = 1.32956e7, 101325       # specific enthalpy, pressure
gas1.UV = 8.34619e6, 1/0.0204723  # specific internal energy, specific volume
gas1.SP = 85227.6, 101325         # specific entropy, pressure
gas1.SV = 85227.6, 1/0.0204723    # specific entropy, specific volume

# %% [markdown]
# Cantera can set and get properties on a molar basis (J/kmol) or a mass basis (J/kg). Note that the mass basis is set by default, so all the values in the previous cell are per unit mass. The basis of a `Solution` instance can be changed by assigning to the `basis` attribute of the instance:

# %%
gas1.basis = 'molar'
gas1.basis = 'mass'

# %% [markdown]
# Properties may be also **read** independently, such as

# %%
gas1.T

# %% [markdown]
# or

# %%
gas1.h

# %% [markdown]
# or together:

# %%
gas1.UV

# %% [markdown]
# The composition can be set in terms of either mole fractions (`X`) or mass fractions (`Y`) by assigning to the corresponding attribute of the `Solution` instance. There are three main options to set the composition of a mixture:
#
# * A string specifying the species names and relative mole numbers
#
#       "CH4:1, O2:2, N2:7.52"
#
# * A Python dictionary where the keys are species names and the values are relative mole numbers
#
#       {"CH4": 1, "O2": 2, "N2": 7.52}
#
# * A NumPy array of length `n_species`
#
# In any of these case, the mole numbers are normalized so the sum is 1.0.

# %%
gas1.X = "CH4:0.8, O2:2, N2:7.52"
print(gas1.mole_fraction_dict())

# %%
gas1.X = {'CH4':0.8, 'O2':2, 'N2': 7.52}
print(gas1.mole_fraction_dict())

# %%
nsp = gas1.n_species
gas1.Y = np.ones(nsp)
gas1()

# %% [markdown]
# When the composition alone is changed, the **temperature** and **density** are held constant. This means that the pressure and other intensive properties will change. The composition can also be set in conjunction with the intensive properties of the mixture:

# %%
gas1.TPX = 1200, 101325, "CH4:1, O2:2, N2:7.52"
gas1()

# %% [markdown]
# When setting the state, you can control what properties are held constant by passing the special value `None` to the property setter. For example, to change the specific volume to 2.1 m<sup>3</sup>/kg while holding entropy constant:

# %%
gas1.SV = None, 2.1
gas1()

# %% [markdown]
# Or to set the mass fractions while holding temperature and pressure constant:

# %%
gas1.TPY = None, None, "CH4:1.0, O2:0.5"

# %% [markdown]
# ### Working with a Subset of Species

# %%
print(gas1.species())

# %% [markdown]
# Many properties of a [`Solution`](https://cantera.org/documentation/docs-2.4/sphinx/html/cython/importing.html#cantera.Solution) provide values for each species present in the phase. If you want to get values only for a subset of these species, you can use Python's "slicing" syntax to select data for just the species of interest. To get the mole fractions of just the major species in `gas1`, in the order specified, you can write:

# %%
Xmajor = gas1['CH4','O2','CO2','H2O','N2'].X
print(Xmajor)

# %% [markdown]
# If you want to use the same set of species repeatedly, you can keep a reference to the sliced phase object:

# %%
major = gas1['CH4','O2','CO2','H2O','N2']
cp_major = major.partial_molar_cp
wdot_major = major.net_production_rates
print(wdot_major)

# %% [markdown]
# The slice object and the original object share the same internal state, so modifications to one will affect the other.

# %%
gas1.TPX = 1200, 101325, "CH4:1, N2:7.52, O2:2"
print(major.net_production_rates)
print(major.X)

# %% [markdown]
# ### Working with Mechanism Files

# %% [markdown]
# In the previous example, we created an object that models an ideal gas mixture with the species and reactions of GRI-Mech 3.0, using the `gri30.yaml` input file included with Cantera. This is a CTI input file and is relatively easy for humans to read and write. Cantera also supports an XML-based input file format that is easy for Cantera to parse, but hard for humans to write. Several reaction mechanism files in both formats are included with Cantera, including ones that model high-temperature air, a hydrogen/oxygen reaction mechanism, and a few surface reaction mechanisms. These files are usually located in the `data` subdirectory of the Cantera installation directory, e.g., `C:\Program Files\Cantera\data` on Windows or `/usr/local/cantera/data/` on Unix/Linux/Mac OS X machines, depending on how you installed Cantera and the options you specified.
#
# There are a number of mechanism files included with Cantera, including the `gri30.yaml` example we saw earlier.

# %%
from pathlib import Path
p = Path(ct.__file__)
print([c.name for c in (p.parent / "data").glob("*.yaml")])

# %% [markdown]
# Cantera input files are plain text files, and can be created with any text editor. See the document *[Defining Phases](https://cantera.org/tutorials/cti/defining-phases.html)* for more information.
#
# A Cantera input file may contain more than one phase specification, or may contain specifications of interfaces (surfaces). Here, we import definitions of two bulk phases and the interface between them from the file `diamond.yaml`:

# %%
gas2 = ct.Solution('diamond.yaml', 'gas')
diamond = ct.Solution('diamond.yaml', 'diamond')
diamond_surf = ct.Interface('diamond.yaml', 'diamond_100', [gas2, diamond])

# %% [markdown]
# Note that the bulk (i.e., 3D or homogenous) phases that participate in the surface reactions must also be passed as arguments to [`Interface`](http://cantera.github.io/docs/sphinx/html/cython/importing.html#cantera.Interface).

# %% [markdown]
# #### Converting CK-format files

# %% [markdown]
# Cantera also comes with a script to convert CHEMKIN (CK)-format input files to the Cantera YAML format. We'll cover that in the [`chemkin_conversion.ipynb`](chemkin_conversion.ipynb) Notebook.

# %% [markdown]
# ### Getting Help

# %% [markdown]
# In addition to the Sphinx-generated *[Python Module Documentation](https://cantera.org/documentation/docs-2.4/sphinx/html/index.html)*, documentation of the Python classes and their methods can be accessed from within the Python interpreter as well.
#
# Suppose you have created a Cantera object and want to know what methods are available for it, and get help on using the methods:

# %%
g = ct.Solution("gri30.yaml")

# %% [markdown]
# To get help on the Python class that this object is an instance of, put a question mark `?` after the variable:

# %%
# g?

# %% [markdown]
# For a simple list of the properties and methods of this object:

# %%
dir(g)

# %% [markdown]
# To get help on a specific method, e.g. the `species_index` method:

# %%
# g.species_index?

# %% [markdown]
# For properties, getting the documentation is slightly trickier, as the usual method will give you help for the *result*, e.g.:

# %%
# g.T?

# %% [markdown]
# provides help on Python's `float` class. To get the help for the temperature property, ask for the attribute of the class object itself:

# %%
# g.__class__.T?

# %% [markdown]
# Help can also be obtained using the `help` function:

# %%
help(g.species_index)

# %% [markdown]
# ### Chemical Equilibrium

# %% [markdown]
# To set a gas mixture to a state of chemical equilibrium, use the `equilibrate` method:

# %%
g = ct.Solution("gri30.yaml")
g.TPX = 300.0, ct.one_atm, "CH4:0.95, O2:2, N2:7.52"
g.equilibrate("TP")
g()

# %% [markdown]
# The above statement sets the state of object `g` to the state of chemical equilibrium holding temperature and pressure fixed.

# %% [markdown]
# Other options are:
# * `'HP'` for fixed specific enthalpy and pressure
# * `'UV'` for fixed specific internal energy and specific volume
# * `'SV'` for fixed specific entropy and specific volume
# * `'SP'` for fixed specific entropy and pressure
#
# How can you tell if `equilibrate` has correctly found the chemical equilibrium state? One way is to verify that the net rates of progress of all reversible reactions are zero. Here is the code to do this:

# %%
rf = g.forward_rates_of_progress
rr = g.reverse_rates_of_progress
for i in range(g.n_reactions):
    if g.is_reversible(i) and rf[i] != 0.0:
        print(f"{i:4d}\t{(rf[i] - rr[i])/rf[i]:10.4g}")

# %% [markdown]
# If the magnitudes of the numbers in this list are all very small (which in this case they are), then each reversible reaction is very nearly equilibrated, which only occurs if the gas is in chemical equilibrium.
#
# You might be wondering how `equilibrate` works. (Then again, you might not.) Method `equilibrate` invokes Cantera's chemical equilibrium solver, which uses an element potential method. The element potential method is one of a class of equivalent *nonstoichiometric* methods that all have the characteristic that the probelm reduces to solving a set of $M$ nonlinear algebraic equations, where $M$ is the number of elements (not species). The so-called *stoichiometric* methods, on the other hand (including the Gibbs minimization), require solving $K$ nonlinear equations, where $K$ is the number of species (usually $K >> M$). See Smith and Missen's "Chemical Reaction Equilibrium Analysis" for more information on the various algorithms and their characteristics.
#
# Cantera uses a damped Newton method to solve these equations, and does a few other things to generate a good starting guess and to produce a reasonably robust algorithm. If you want to know more about the details, look at the on-line documentated source code of Cantera C++ class [`ChemEquil.h`](https://cantera.org/documentation/docs-2.4/doxygen/html/d4/dd4/ChemEquil_8h.html).

# %%
