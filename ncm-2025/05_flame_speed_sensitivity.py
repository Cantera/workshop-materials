# %% [markdown]
# ## Flame Speed

# %% [markdown]
# In this example we simulate a freely-propagating, adiabatic, 1-D flame and
# * Calculate its laminar burning velocity
# * Perform a sensitivity analysis of its kinetics
#
# The figure below illustrates the setup, in a flame-fixed co-ordinate system. The reactants enter with density $\rho_{u}$, temperature $T_{u}$ and speed $S_{u}$. The products exit the flame at speed $S_{b}$, density $\rho_{b}$ and temperature $T_{b}$.

# %% [markdown]
# <img src="https://github.com/Cantera/workshop-materials/blob/ncm-2025/ncm-2025/images/flameSpeed.png?raw=true" alt="Freely Propagating Flame" style="width: 300px; background: white; border:5px solid white"/>

# %% [markdown]
# #### Import Modules

# %%
import cantera as ct
import numpy as np
import pandas as pd

# %matplotlib inline
import matplotlib.pyplot as plt
plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams['lines.linewidth'] = 2

print(f"Running Cantera version {ct.__version__}")

# %% [markdown]
# #### Define the reactant conditions, gas mixture and kinetic mechanism associated with the gas

# %%

# %% [markdown]
# #### Define flame simulation conditions

# %%

# %% [markdown]
# #### Solve

# %% [markdown]
# The `auto` option in the solve function tries to "automatically" solve the flame by applying a few common techniques. First, the flame is solved on a sparse grid with the transport calculations set to mixture averaged. Then grid refinement is enabled, with points added according to the values of the `ratio`, `slope`, and `curve` parameters in the `set_refine_criteria` function. If the initial solve on the sparse grid fails to converge, the simulation is attempted again, but this time with the energy equation disabled. Once the simulation has been solved on the refined grid with the mixture averaged transport, Cantera enables the multicomponent transport and Soret diffusion, if they have been set by the user.
#
# In general, it is recommended that you use the `auto` option the first time you run the solver, unless the simulation fails. On subsequent invocations of `solve`, you should not include the `auto` option (or set it to `False`).

# %%

# %%

# %% [markdown]
# #### Plot figures
#
# Check and see if all has gone well. Plot temperature and species fractions to see. We expect that the solution at the boundaries of the domain will have zero gradient (in other words, that the domain width that we specified is wide enough for the flame).

# %% [markdown]
# ##### Temperature Plot

# %%

# %% [markdown]
# ##### Major species' plot

# %%

# %% [markdown]
# ### Sensitivity analysis
# Compute normalized sensitivities of flame speed $S_u$ to changes in the rate coefficient $k_i$ for each reaction
# $$s_i = \frac{k_i}{S_u} \frac{d S_u}{d k_i} $$
#
# See details about the adjoint method for flame speed sensitivity at https://cantera.org/3.1/examples/python/onedim/flamespeed_sensitivity.html.

# %%

# %%

# %% [markdown]
# ### Solving multiple flames (parameter sweep)

# %%

# %%

# %%

# %%
