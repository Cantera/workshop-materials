# %% [markdown]
# ## Plasma Phase
#
# Plasma is the fourth state of matter. A non-equilibrium plasma is a plasma with the electron temperature much higher than the gas temperature. The energy distribution of electron energy of non-equilibrium plasmas can be non-maxwellian depends on the electric/magnetic field and the gas molecules. PlasmaPhase manages the **electron energy distribution function (EEDF)**, which is used for calculating plasma properties.
#
# ### Isotropic velocity
#
# The generalized isotropic-velocity electron energy distribution is given by:
# $$
# f(\epsilon) = c_1 \frac{\sqrt{\epsilon}}{\epsilon_m^{3/2}}
#          \exp \left(-c_2 \left(\frac{\epsilon}{\epsilon_m}\right)^x \right),
# $$
# where:
# - $\epsilon$ is the electron energy,
# - $\epsilon_m$ is the mean electron energy ($\epsilon_m = \frac{3}{2} T_e$),
# - $F_0$ is the normalized electron energy distribution function,
# - $x = 1$ corresponds to a Maxwellian distribution, while $x = 2$ corresponds to a Druyvesteyn distribution.
# - $c_1 = x \cdot \frac{\Gamma\left(\frac{5}{2} x\right)^{1.5}}{\Gamma\left(\frac{3}{2} x\right)^{2.5}}$
# - $c_2 = \cdot \left( \frac{\Gamma\left(\frac{5}{2} x\right)}{\Gamma\left(\frac{3}{2} x\right)} \right)^x$
#
# In Cantera, the electron energy probability function is defined as $F(\epsilon) = f(\epsilon) \sqrt{\epsilon}$. The generalized form of the electron energy probability function for isotropic velocity distributions is:
# $$
# F(\epsilon) = c_1 \frac{1}{\epsilon_m^{3/2}}
#          \exp \left(-c_2 \left(\frac{\epsilon}{\epsilon_m}\right)^x \right).
# $$
#
# #### Example YAML Definition
#
# ```yaml
# - name: isotropic-electron-energy-plasma
#   thermo: plasma
#   elements: [O, E]
#   species:
#   - species: [e, O2(a1)]
#   - nasa_gas.yaml/species: [O, O2, O2-, O-, O2+]
#
#   kinetics: gas
#   reactions:
#   - reactions: all
#   - collisions: all
#   transport: Ion
#   state: {T: 300.0, P: 0.01 atm}
#   electron-energy-distribution:
#     type: isotropic
#     shape-factor: 1.0
#     mean-electron-energy: 2.0 eV
#     energy-levels: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
#                     2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
#                     11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0,
#                     18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0]
# ```
#
# ### Anisotropic velocity
# Two-term approximation method is a good approximation. Cantera provide interfaces for user to input the energy distribution with function `setDiscretizedElectronEnergyDist()` or specify in a YAML file.
#
#
#
# For more details, see the [Cantera PlasmaPhase documentation](https://cantera.org/dev/cxx/d5/dd7/classCantera_1_1PlasmaPhase.html).

# %% [markdown]
# ### Why plasma phase in Cantera?
# * Cantera has better reaction data management
# * Cantera has better kinetics, thermodynamic, and transport integration
# * Plasma assisted combustion - intersection of plasma and combustion

# %%
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# #### Define the plasma phase

# %%
plasma = ct.Solution('../inputs/oxygen-plasma.yaml', 'isotropic-electron-energy-plasma', transport_model=None)

# %% [markdown]
# #### Plot the original EEDF

# %%
plt.plot(plasma.electron_energy_levels,
         plasma.electron_energy_distribution * np.sqrt(plasma.electron_energy_levels),
         lw=2, marker='s', markersize=4, label='Mean Electron Energy = 2 eV')

# Labels and legend
plt.xlabel('Electron Energy [eV]')
plt.ylabel('Distribution Function [1/eV]')

# %% [markdown]
# #### Adjust the electron energy distribution function
# * mean electron energy
# * energy grid

# %%
plasma.mean_electron_energy = 5.0
plasma.isotropic_shape_factor = 2.0
plasma.electron_energy_levels = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                    1.2, 1.4, 1.6, 1.8, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0,
                    10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0,
                    18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0]

# %% [markdown]
# #### Plot the adjusted EEDF

# %%
plt.plot(plasma.electron_energy_levels,
        plasma.electron_energy_distribution * np.sqrt(plasma.electron_energy_levels),
        lw=2, marker='s', markersize=4, label='Mean Electron Energy = 2 eV')

# Labels and legend
plt.xlabel('Electron Energy [eV]')
plt.ylabel('Distribution Function [1/eV]')

# %% [markdown]
# ## Electron Collision Plasma Reaction
#
# <img src="https://github.com/Cantera/workshop-materials/blob/ncm-2025/ncm-2025/images/plasma-reactions.png?raw=true" alt="Plasma Reactions" width="600" height="400" style="750px; background: white; border:5px solid white">
#
# **Image from:** Gerhard, C., Viöl, W., & Wieneke, S. (2016). *Plasma Science and Technology: Progress in Physical States and Chemical Reactions, 1.*
#
# The electron collision plasma reaction rate uses the electron collision data and the electron energy distribution to calculate the reaction rate. For more details, visit [Cantera Electron Collision Plasma Rate](https://cantera.org/dev/cxx/d9/ddb/classCantera_1_1ElectronCollisionPlasmaRate.html).
#
# The general form of the reaction rate is given by:
#
# $$
# k_f = \gamma N_A \int_0^{\infty} \epsilon \sigma F_0 d\epsilon,
# $$
#
# where:
# - $ N_A $ is the Avogadro number,
# - $ \sigma $ is the reaction collision cross section,
# - $ F_0 $ is the electron energy distribution function.
#
# In addition to the forward reaction coefficient, the reverse (super-elastic) reaction coefficient can be written as:
#
# $$
# k_r = \gamma N_A \int_0^{\infty} \epsilon \sigma_{super} F_0 d\epsilon,
# $$
#
# where $ \sigma_{super} $ is the super-elastic cross section, defined by the principle of detailed balancing as:
#
# $$
# \sigma_{super}(\epsilon) = \frac{\epsilon + U}{\epsilon} \sigma(\epsilon + U),
# $$
#
# with $ U $ being the threshold energy.
#
# ---
#
# The corresponding YAML input file section is demonstrated below:
#
# ```yaml
# collisions:
# - equation: O2 + e => e + O2
#   type: electron-collision-plasma
#   note: elastic collision
#   energy-levels: [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 15.0, 20.0]
#   cross-sections: [0.0, 5.97e-20, 6.45e-20, 6.74e-20, 6.93e-20, 7.2e-20, 7.52e-20,
#                    7.86e-20, 8.21e-20, 8.49e-20, 8.8e-20, 9.0e-20, 8.89e-20, 8.6e-20]
# - equation: O2 + e => O- + O
#   type: electron-collision-plasma
#   note: dissociative attachment
#   energy-levels: [4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2,
#     5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.5, 6.6, 6.7, 6.8, 6.9,
#     7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5,
#     8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.8, 9.9]
#   cross-sections: [0.0, 8.8e-25, 2.64e-24, 4.4e-24, 7.04e-24, 9.68e-24, 1.32e-23,
#     1.76e-23, 2.2e-23, 2.9e-23, 3.61e-23, 4.49e-23, 5.37e-23, 6.33e-23, 7.48e-23,
#     8.53e-23, 9.59e-23, 1.05e-22, 1.14e-22, 1.23e-22, 1.31e-22, 1.36e-22, 1.41e-22,
#     1.4e-22, 1.37e-22, 1.34e-22, 1.28e-22, 1.22e-22, 1.14e-22, 1.06e-22, 9.85e-23,
#     8.97e-23, 8.18e-23, 7.39e-23, 6.42e-23, 5.72e-23, 5.01e-23, 4.49e-23, 3.87e-23,
#     3.34e-23, 2.82e-23, 2.38e-23, 2.02e-23, 1.67e-23, 1.41e-23, 1.23e-23, 1.06e-23,
#     8.8e-24, 7.04e-24, 7.04e-24, 6.16e-24, 5.28e-24, 4.4e-24, 4.4e-24, 3.52e-24, 3.52e-24]
# - equation: O2 + e => e + e + O2+
#   type: electron-collision-plasma
#   note: ionization
#   energy-levels: [12.06, 13.0, 15.5, 18, 23]
#   cross-sections: [0.0, 1.17e-22, 7.3e-22, 1.64e-21, 3.66e-21]
# - equation: O2 + e => e + O + O
#   type: electron-collision-plasma
#   note: dissociation
#   energy-levels: [6.12, 13.5, 18.5, 21.0, 23.5]
#   cross-sections: [0.0, 2.2e-21, 5.29e-21, 5.65e-21, 5.25e-21]
# - equation: O2 + e => O2(a1) + e
#   type: electron-collision-plasma
#   note: excitation
#   energy-levels: [0.977, 5.0, 7.0, 10.0, 15.0, 20.0]
#   cross-sections: [0.0, 7.6e-22, 1.04e-21, 7.7e-22, 4.2e-22, 2.3e-22]
# ```
#

# %% [markdown]
# #### Check reaction equation

# %%
plasma.reaction(10)

# %% [markdown]
# #### Check reaction rate constant

# %%
plasma.forward_rate_constants[10]

# %% [markdown]
# #### Check ECPR cross sections

# %%
reaction = plasma.reaction(10)
plt.plot(reaction.rate.energy_levels, reaction.rate.cross_sections, lw=2, marker='s', markersize=4)

# Labels and legend
plt.xlabel('Electron Energy [eV]')
plt.ylabel('Cross Section [m²]')

# %% [markdown]
# ## Plasma Properties Dependent on Electron Collision Plasma Reactions
#
# Plasma properties, such as the electron energy loss coefficient, depend on electron collision plasma reactions (ECPR). The **Plasma Phase** can now utilize ECPR data to calculate these properties.
#
# In an ECPR, a neutral particle can gain kinetic energy through collisions, while the electron loses energy accordingly (excluding inelastic energy transfers such as excitation). For each ECPR in a plasma, the **elastic electron energy loss coefficient** (eV·m³/s) is given by:
# $$
#      K_k = \frac{2 m_e}{m_k} \sqrt{\frac{2 e}{m_e}} \int_0^{\infty} \sigma_k
#            \epsilon^2 \left( F_0 + \frac{k_B T}{e}
#            \frac{\partial F_0}{\partial \epsilon} \right) d \epsilon,
# $$
# where:
# - $m_e$ [kg] is the electron mass,
# - $\epsilon$ [V] is the electron energy,
# - $\sigma_k$ [m²] is the reaction collision cross-section,
# - $F_0$ [V\(^{-3/2}\)] is the normalized electron energy distribution function.
#
# The total **elastic power loss** (J/s/m³) is given by:
# $$
#      P_k = N_A N_A C_e e \sum_k C_k K_k,
# $$
# where:
# - $C_k$ and $C_e$ are the concentrations (kmol/m³) of the target species and electrons, respectively,
# - $K_k$ is the elastic electron energy loss coefficient (eV·m³/s).

# %% [markdown]
# #### Define plasma composition

# %%
plasma.TPX = 300, ct.one_atm, "O2:1, e:1e-6"

# %% [markdown]
# #### Get plasma properties
# * electron temperature
# * elastic power loss (electron to molecules)

# %%
plasma.Te

# %%
plasma.elastic_power_loss
