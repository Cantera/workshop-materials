# %%

# %% [markdown]
# ## Mechanism files & basic info
#
# https://github.com/Cantera/cantera/blob/main/data/gri30.yaml

# %%

# %%

# %%

# %% [markdown]
# ## Species thermo data
#
# NASA 7-coefficient polynomials:
#
# $$   \frac{\hat{c}_p^\circ(T)}{\overline{R}} = a_0 + a_1 T + a_2 T^2 + a_3 T^3 + a_4 T^4 $$
#
# $$   \frac{\hat{h}^\circ (T)}{\overline{R} T} = a_0 + \frac{a_1}{2} T + \frac{a_2}{3} T^2 +
#                          \frac{a_3}{4} T^3 + \frac{a_4}{5} T^4 + \frac{a_5}{T} $$
#
# $$   \frac{\hat{s}^\circ(T)}{\overline{R}} = a_0 \ln T + a_1 T + \frac{a_2}{2} T^2 + \frac{a_3}{3} T^3 +
#                       \frac{a_4}{4} T^4 + a_6 $$

# %%

# %%

# %%

# %%

# %% [markdown]
# ## Setting thermodynamic state
# - Always requires two variables, e.g. $(T, P)$ or $(T, v)$ or $(s, P)$ etc.
# - Specify `None` to hold a property constant
#
# https://cantera.org/documentation/docs-3.0/sphinx/html/cython/thermo.html#thermophase

# %%

# %%

# %%

# %% [markdown]
# ## Setting composition
# - Main ways are by setting either mass fractions ($Y$) or mole fractions ($X$)
# - Can be set alone (in which case $(T,\rho)$ held constant), or with a valid property pair
# - Mass/mole fractions are automatically normalized to 1.0
# - Can also set equivalence ratio

# %%

# %%

# %%

# %%

# %%

# %% [markdown]
# ## Flame temperature calculation
#
# With a guest appearance by the `SolutionArray` class.

# %%

# %%

# %%

# %%

# %%

# %% [markdown]
# ## Kinetics & Reactions
#
# https://cantera.org/documentation/docs-3.0/sphinx/html/cython/kinetics.html#kinetics

# %%

# %%

# %%

# %%

# %%

# %% [markdown]
# ## Defining reactions & exploring equilibrium
#
# $$ a \mathrm{A} + b \mathrm{B} \rightleftharpoons c \mathrm{C} + d \mathrm{D} $$
#
# $$ \Delta_r^\circ \hat{g} = \Delta_r^\circ \hat{h} - T \Delta_r^\circ \hat{s}$$
#
# $$ K_c = \frac{k_f}{k_r} = \frac{[\mathrm{C}]^c [\mathrm{D}]^d}{[\mathrm{A}]^a [\mathrm{B}]^b} = \exp\left( \frac{\Delta_r^\circ \hat{g}}{RT} \right) \left( \frac{p^o}{RT}\right)^{\nu_{net}} $$

# %%

# %%

# %%

# %%
