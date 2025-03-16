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

# %% [markdown]
# These warnings are part of a validation check that Cantera does to make sure the thermodynamics data are consistent. In the standard NASA 14-coefficient polynomial form, the thermodynamics data are defined as two five coefficient polynomials (plus two other constants) over two temperature ranges. This is the form used for CHEMKIN files. The discontinuities occur when either the slope or the value of the thermodynamic functions ($c_p/R$, $h/(RT)$, or $s/R$) has a discontinuity at the mid-point temperature. Most commonly, one or more the discontinuities are due to incorrectly fit parameters, but they can also be caused by other means. Let's investigate.

# %%

# %%

# %%

# %%

# %%

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

# %%

# %% [markdown]
# There are clearly several reverse rates with very high magnitudes. Let's print the reactions with reverse rate constants higher than $10^{20}$:

# %%

# %% [markdown]
# Among these is the reaction
#
# $$\text{CH}_3 + \text{M} <=> \text{CH} + \text{H}_2 + \text{M}$$
#
# with reverse rate constant of `4.2656e+23`. This is a pretty common reaction, so we can compare to the same reaction from, for example, GRI 3.0:

# %%

# %% [markdown]
# The reaction is #295 from the first mechanism and #288 from GRI 3.0. We can calculate the rate of each reaction over a range of temperatures from 300 K to 3000 K and plot them.

# %%

# %% [markdown]
# Here, we see that the rate of the reactions is close-ish at high temperature (>1000 K), but as the temperature decreases, they rapidly diverge and differ by 11 orders of magnitude at 300 K. This can cause problems in the integrator for both 0-D and 1-D problems, often accompanied by error messages about "Repeated recoverable right-hand side errors"
