# %% [markdown]
# ## Preconditioners for faster reactor integration
#
# This demos the relatively new feature in Cantera v3.0.0 that offers a preconditioned, iterative linear solver to replace the direct linear solver in reactor integration. For more on this approach, you can read about the method in detail:
# > Anthony S. Walker, Raymond L. Speth, and Kyle E. Niemeyer. 2023. “Generalized preconditioning for accelerating simulations with large kinetic models.” *Proceedings of the Combustion Institute*, 39(4):5395–5403. https://doi.org/10.1016/j.proci.2022.07.256
#
#
# Here, we will compare the times for simulating ignition of a stoichiometric n-hexane/air mixture, 
# using a detailed chemical kinetic model with 1268 species, between the default integration approach 
# and the preconditioned solver. We'll also compare the resulting profiles of temperature and 
# some species mass fractions, to confirm that they agree extremely closely. 
# (In fact, they essentially agree within the expected numerical error of integration, 
# since the same governing equations are being solved—the only changes are happening 
# in the linear algebra solver used within the time-integration algorithm.)


# %% [markdown]
# #### Import packages

# %%
import cantera as ct
import matplotlib.pyplot as plt
import numpy as np
from timeit import default_timer
ct.__version__

# %% [markdown]
### Start with default strategy 
# First, we'll solve a homogeneous ignition problem using the default integration strategy, 
# which internally uses a direct linear solver.

# %% [markdown]
# Load the detailed n-hexane mechanism with 1268 species.
# Set initial conditions of 1000 K, 1 atm, and stoichometric mixture of fuel & air, 
# and establish the `Reactor` and `ReactorNet` objects.

# %%
gas = ct.Solution('../inputs/n-hexane-NUIG-2015.yaml')
gas.TP = 1000, ct.one_atm
gas.set_equivalence_ratio(1, 'NC6H14', 'N2:3.76, O2:1.0')
reactor = ct.IdealGasConstPressureMoleReactor(gas)
reactor.volume = 0.1

# Create reactor network
sim = ct.ReactorNet([reactor])
sim.initialize()

# Integrate to 0.1 sec
end_time = 0.1

# %%
# Integrate to steady state, using a timer and storing output in `SolutionArray`
integ_time = default_timer()
states = ct.SolutionArray(reactor.thermo, extra=['time'])
while (sim.time < end_time):
    states.append(reactor.thermo.state, time=sim.time)
    sim.step()
integ_time = default_timer() - integ_time

print(f"Non-preconditioned integration time: {integ_time:f}")

# %% [markdown]
# ### Now, let's switch to a sparse, iterative solver with preconditioning:

# %%
gas = ct.Solution('../inputs/n-hexane-NUIG-2015.yaml')
gas.TP = 1000, ct.one_atm
gas.set_equivalence_ratio(1, 'NC6H14', 'N2:3.76, O2:1.0')
reactor = ct.IdealGasConstPressureMoleReactor(gas)
reactor.volume = 0.1
sim = ct.ReactorNet([reactor])

# %% [markdown]
# We need to instantiate the preconditioner and pass in some options for 
# the approximations used by it. The preconditioner is based on the Jacobian matrix for
# the chemical kinetics ODE system, with some approximations applied to simplify calculation and 
# increase sparsity of the matrix.
#
# You can read more details and additional customization options for the 
# [`AdaptivePreconditioner`](https://cantera.org/stable/python/zerodim.html#cantera.AdaptivePreconditioner) 
# class, and options for approximating derivatives in the chemical kinetic Jacobian in 
# [`Kinetics.derivative_settings`](https://cantera.org/stable/python/kinetics.html#cantera.Kinetics.derivative_settings)
# property.
#
# Here, we will use some default options and common approximations, by neglecting third-body efficiencies 
# in three-body and pressure-dependent reactions in forming the Jacobian. Note that this does *not* change
# the actual governing equations being integrated—just what is used for the preconditioner internally.

# %%
# Specify precondioner approximations
sim.derivative_settings = {
    "skip-third-bodies":True, 
    "skip-falloff":True
    }
# 
sim.preconditioner = ct.AdaptivePreconditioner()

sim.initialize()

# %%
integ_time_pre = default_timer()
states_pre = ct.SolutionArray(reactor.thermo, extra=['time'])
while (sim.time < end_time):
    states_pre.append(reactor.thermo.state, time=sim.time)
    sim.step()
integ_time_pre = default_timer() - integ_time_pre

print(f"Preconditioned integration time: {integ_time_pre:f}")


# %% [markdown]
# Let's compare the results to make sure they agree closely.

# %%
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5, 8))

# temperature plot
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature")
ax1.plot(states.time, states.T, linewidth=2)
ax1.plot(states_pre.time, states_pre.T, linewidth=2, linestyle=":")
ax1.legend(["Normal", "Preconditioned"])

# CO2 plot
ax2.set_xlabel("Time")
ax2.set_ylabel("CO2 mass fraction")
ax2.plot(states.time, states('CO2').Y, linewidth=2)
ax2.plot(states_pre.time, states_pre('CO2').Y, linewidth=2, linestyle=":")
ax2.legend(["Normal", "Preconditioned"])

# NC6H14 plot
ax3.set_xlabel("Time")
ax3.set_ylabel("NC6H14 mass fraction")
ax3.plot(states.time, states('NC6H14').Y, linewidth=2)
ax3.plot(states_pre.time, states_pre('NC6H14').Y, linewidth=2, linestyle=":")
ax3.legend(["Normal", "Preconditioned"])
plt.tight_layout()
plt.show()

# %%
