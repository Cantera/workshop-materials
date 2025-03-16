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

# %%
import cantera as ct
import numpy as np

# %matplotlib widget
import matplotlib.pyplot as plt
plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams['lines.linewidth'] = 2

# %% [markdown]
# ## Thermo Data

# %% [markdown]
# When loading a YAML file, sometimes you will encounter warnings about discontinuities in the thermodynamic data.

# %%
gas = ct.Solution('../inputs/mech_debug/mech.yaml')

# %% [markdown]
# These warnings are part of a validation check that Cantera does to make sure the thermodynamics data are consistent. In the standard NASA 14-coefficient polynomial form, the thermodynamics data are defined as two five coefficient polynomials (plus two other constants) over two temperature ranges. This is the form used for CHEMKIN files. The discontinuities occur when either the slope or the value of the thermodynamic functions ($c_p/R$, $h/(RT)$, or $s/R$) has a discontinuity at the mid-point temperature. Most commonly, one or more the discontinuities are due to incorrectly fit parameters, but they can also be caused by other means. Let's investigate.

# %%
ct.suppress_thermo_warnings()

# %%
sp = gas.species('H2CNO')
T = np.linspace(600, 2000, 200)
f,ax = plt.subplots(1,3, figsize=(8,3.5))

def plot_thermo(thermo):
    h = [thermo.h(tt)/(ct.gas_constant * tt) for tt in T]
    cp = [thermo.cp(tt)/ct.gas_constant for tt in T]
    s = [thermo.s(tt)/ct.gas_constant for tt in T]
    ax[0].plot(T,cp)
    ax[0].set_title('$c_p/R$')
    ax[1].plot(T,h)
    ax[1].set_title('$h/RT$')
    ax[2].plot(T,s)
    ax[2].set_title('$s/R$')
plot_thermo(sp.thermo)

# %%
c0 = sp.thermo.coeffs
c0

# %%
c0[0] = 1200
test = ct.NasaPoly2(sp.thermo.min_temp, sp.thermo.max_temp, sp.thermo.reference_pressure, c0)
plot_thermo(test)

# %%
c0[0] = 1000
test = ct.NasaPoly2(sp.thermo.min_temp, sp.thermo.max_temp, sp.thermo.reference_pressure, c0)
plot_thermo(test)

# %% [markdown]
# In many cases, when the change is on the order of a few percent, these discontinuities won't cause problems. However, if you notice a simulation failing at a consistent temperature for several conditions, this is one possible cause.

# %% [markdown]
# ## Reaction Rates

# %% [markdown]
# Another common issue with mechanisms are unphysical reaction rates (particularly reverse reaction rates). These unphysical reaction rates often exceed the collision limit for a given reaction. A recent(ish) study by [Chen et al.](https://www.sciencedirect.com/science/article/pii/S0010218017303024) found that
#
# > among.. 20 [recent] models tested, 15 of them contain either considerable numbers of rate coefficients that exceed their respective collision limits or reactions exceeding the collision limit in a considerable manner. In the worst case, the rate coefficient exceeds the collision limit by 73 orders of magnitude.
#
# The authors continue
#
# > It is proposed that computational tools should be made available for authors to conduct the same rate coefficient screening.
#
# Let's take a look at how Cantera can fill this need.

# %%
gas.TPX = 300, 101325, 'CH4:1.0, O2:0.1'
gas.equilibrate('TP')
gas()

# %%
f, ax = plt.subplots()
ax.semilogy(gas.forward_rate_constants, '.', label='forward')
ax.semilogy(gas.reverse_rate_constants, '.', label='reverse')
ax.axis(ymin=1e-30)
ax.legend();

# %% [markdown]
# There are clearly several reverse rates with very high magnitudes. Let's print the reactions with reverse rate constants higher than $10^{20}$:

# %%
kr = gas.reverse_rate_constants
for i, k in enumerate(kr):
    if k > 1e20:
        print(f'{i:4d}  {k:.4e}  {gas.reaction(i).equation}')

# %% [markdown]
# Among these is the reaction 
#
# $$\text{CH}_3 + \text{M} <=> \text{CH} + \text{H}_2 + \text{M}$$
#
# with reverse rate constant of `4.2656e+23`. This is a pretty common reaction, so we can compare to the same reaction from, for example, GRI 3.0:

# %%
gri = ct.Solution('gri30.yaml')
for i, R in enumerate(gri.reactions()):
    if 'CH3' in R and 'H2' in R and 'CH' in R:
        print(i, R)

# %% [markdown]
# The reaction is #295 from the first mechanism and #288 from GRI 3.0. We can calculate the rate of each reaction over a range of temperatures from 300 K to 3000 K and plot them.

# %%
gasN = ct.SolutionArray(gas, shape=200)
griN = ct.SolutionArray(gri, shape=200)
T = np.linspace(300, 3000, 200)
gasN.TPY = T, ct.one_atm, 'N2:1.0'
griN.TPY = T, ct.one_atm, 'N2:1.0'

f,ax = plt.subplots()
ax.semilogy(1000/T, gasN.forward_rate_constants[:,295], label='mech, forward')
ax.semilogy(1000/T, gasN.reverse_rate_constants[:,295], label='mech, reverse')
ax.semilogy(1000/T, griN.forward_rate_constants[:,288], '--', label='GRI 3.0, forward')
ax.semilogy(1000/T, griN.reverse_rate_constants[:,288], '--', label='GRI 3.0, reverse')
T_label = np.array([300, 400, 500, 700, 1000, 2000])
ax.set(xticks=1000/T_label, xticklabels=T_label, xlabel='Temperature (K)')
ax.legend()
ax.grid(True)

# %% [markdown]
# Here, we see that the rate of the reactions is close-ish at high temperature (>1000 K), but as the temperature decreases, they rapidly diverge and differ by 11 orders of magnitude at 300 K. This can cause problems in the integrator for both 0-D and 1-D problems, often accompanied by error messages about "Repeated recoverable right-hand side errors"
