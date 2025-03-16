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
# Define the gas mixture and kinetics
# In this case, we are choosing a modified version of GRI 3.0
# gas = ct.Solution('input-files/gri30_noNOx.yaml')
gas = ct.Solution('gri30.yaml')

# %% [markdown]
# #### Define flame simulation conditions

# %%
# Inlet temperature in kelvin and inlet pressure in pascal
To = 300
Po = 101325

# Domain width in meters
width = 0.02

# Set the inlet mixture to be stoichiometric CH4 and air
gas.set_equivalence_ratio(1.0, 'CH4', {'O2':1.0, 'N2':3.76})
gas.TP = To, Po

# Create the flame object
flame = ct.FreeFlame(gas, width=width)

# Set options for the solver
flame.transport_model = 'mixture-averaged'
flame.set_refine_criteria(ratio=3, slope=0.1, curve=0.1)

# Define logging level
loglevel = 1

# %% [markdown]
# #### Solve

# %% [markdown]
# The `auto` option in the solve function tries to "automatically" solve the flame by applying a few common techniques. First, the flame is solved on a sparse grid with the transport calculations set to mixture averaged. Then grid refinement is enabled, with points added according to the values of the `ratio`, `slope`, and `curve` parameters in the `set_refine_criteria` function. If the initial solve on the sparse grid fails to converge, the simulation is attempted again, but this time with the energy equation disabled. Once the simulation has been solved on the refined grid with the mixture averaged transport, Cantera enables the multicomponent transport and Soret diffusion, if they have been set by the user.
#
# In general, it is recommended that you use the `auto` option the first time you run the solver, unless the simulation fails. On subsequent invocations of `solve`, you should not include the `auto` option (or set it to `False`).

# %%
flame.solve(loglevel=loglevel, auto=True)

# %%
Su0 = flame.velocity[0]
print("Flame Speed is: {:.2f} cm/s".format(Su0*100))
flame.show_stats()

# %% [markdown]
# #### Plot figures
#
# Check and see if all has gone well. Plot temperature and species fractions to see. We expect that the solution at the boundaries of the domain will have zero gradient (in other words, that the domain width that we specified is wide enough for the flame).

# %% [markdown]
# ##### Temperature Plot

# %%
# %matplotlib inline
f, ax = plt.subplots(1, 1)
ax.plot(flame.grid*100, flame.T)
ax.set(xlabel='Distance (cm)', ylabel='Temperature (K)');
# note domain size is not what we originally set -- automatically expanded to satisfy boundary conditions

# %% [markdown]
# ##### Major species' plot

# %%
profile = ct.SolutionArray(gas, shape=len(flame.grid), extra={'z': flame.grid*100})
profile.TPY = flame.T, flame.P, flame.Y.T

f, ax = plt.subplots(1, 1)
ax.plot(profile.z, profile('CH4').X, label=r'CH$_4$')
ax.plot(profile.z, profile('O2').X, label=r'O$_2$')
ax.plot(profile.z, profile('CO2').X, label=r'CO$_2$')
plt.plot(profile.z, profile('H2O').X, label=r'H$_2$O')
ax.legend()
ax.set(xlabel='Distance (cm)', ylabel='Mole fraction');

# %% [markdown]
# ### Sensitivity analysis
# Compute normalized sensitivities of flame speed $S_u$ to changes in the rate coefficient $k_i$ for each reaction
# $$s_i = \frac{k_i}{S_u} \frac{d S_u}{d k_i} $$
#
# See details about the adjoint method for flame speed sensitivity at https://cantera.org/3.1/examples/python/onedim/flamespeed_sensitivity.html.

# %%
# Create a DataFrame to store sensitivity-analysis data
sens = pd.DataFrame(index=gas.reaction_equations(), columns=["sensitivity"])

# Use the adjoint method to calculate sensitivities
sens.sensitivity = flame.get_flame_speed_reaction_sensitivities()

# Show the first 10 sensitivities
sens.head(10)

# %%
# Sort the sensitivities in order of descending magnitude
sens = sens.iloc[(-sens['sensitivity'].abs()).argsort()]

fig, ax = plt.subplots()

# Reaction mechanisms can contains thousands of elementary steps. Limit the plot
# to the top 15
sens.head(15).plot.barh(ax=ax, legend=None)

ax.invert_yaxis()  # put the largest sensitivity on top
ax.set_title("Sensitivities for GRI 3.0")
ax.set_xlabel(r"Sensitivity: $\frac{\partial\:\ln S_u}{\partial\:\ln k}$")
ax.grid(axis='x')

# %% [markdown]
# ### Solving multiple flames (parameter sweep)

# %%
# Start  at one limit of the equivalence ratio range
gas.set_equivalence_ratio(0.6, 'CH4', {'O2':1.0, 'N2':3.76})
gas.TP = To, Po

flame = ct.FreeFlame(gas, width=width)

# Enabling pruning is important to avoid continuous increase in grid size
flame.set_refine_criteria(ratio=3, slope=0.15, curve=0.15, prune=0.1)
flame.solve(loglevel=0, refine_grid=True, auto=True)

# %%
phis = np.linspace(0.6, 1.8, 50)
Su = []

for phi in phis:
    gas.set_equivalence_ratio(phi, 'CH4', {'O2':1.0, 'N2':3.76})
    flame.inlet.Y = gas.Y
    flame.solve(loglevel=0)
    print(f'phi = {phi:.3f}: Su = {flame.velocity[0]*100:5.2f} cm/s, N = {len(flame.grid)}')
    Su.append(flame.velocity[0])

# %%
f, ax = plt.subplots(1, 1)
ax.plot(phis, Su)
ax.set(xlabel='equivalence ratio', ylabel='flame speed (m/s)');
