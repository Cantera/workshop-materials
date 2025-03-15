# %% [markdown]
# ### Import packages

# %%
from math import exp
from timeit import default_timer

import cantera as ct
print(f"Using Cantera version {ct.__version__}")

# %% [markdown]
# ## Extensible Reaction Rates
#
# This example demonstrates how to use user-defined reaction rate definitions.
#
# Cantera defines reactions through YAML reaction rate specifications as follows:
#
# # <img src="https://github.com/Cantera/workshop-materials/blob/5110a218d966a907446e8ccd1f06ea132eb5e301/ncm-2025/images/Reactions.png?raw=true" alt="Example for YAML reaction specification." style="width: 750px; border:1px solid white"/>
#
# where kinetics generally follow the Law of Mass Action
#
# $$R_i = k_{\rm fwd}\prod_k C_{k}^{\nu^\prime_{k,i}} - k_{\rm rev}\prod_k C_{k}^{\nu^{\prime\prime}_{k,i}}$$
#
# with $k_{\rm fwd}$ and $k_{\rm rev}$ representing forward and reverse reaction rates (see also: [Cantera Science - Reaction Rates](https://cantera.org/stable/reference/kinetics/reaction-rates.html) documentation).
#
# Cantera provides multiple standard reaction rate parameterizations, where the default is the _modified Arrhenius function_
#
# $$k_{\rm fwd} = AT^b\exp\left(-\frac{E_a}{RT}\right)$$
#
# Additional supported rate parameterizations include, among others, _Falloff Reactions_, _P-Log_ and _Chebyshev_ (see also: [Cantera Science - Rate Constant Parameterizations](https://cantera.org/stable/reference/kinetics/rate-constants.html) documentation).
#
# > **This demo illustrates ways to introduce user-defined rate expressions that are not provided by Cantera.**

# %% [markdown]
# ### Load a Mechanism to Use as Basis
#
# For simplicity, let's use the ${\rm H}_2-{\rm O}_2$ submechanism of `GRI 3.0`, which is available via `h2o2.yaml`. This mechanism will serve as the basis for this demonstration.

# %%
mech = 'h2o2.yaml'  # mechanism file
gas0 = ct.Solution(mech)  # load mechanism
species = gas0.species()  # retrieve all associated species
reactions = gas0.reactions()  # retrieve all associated reactions

fuel = 'H2'  # fuel
oxidizer = 'O2:1.0, N2:3.773'  # oxidizer composition
T = 1000  # temperature
P = 5 * ct.one_atm  # pressure
phi = 0.8  # equivalence ratio

print(f"# of reactions: {gas0.n_reactions}\n# of species: {gas0.n_species}")

# %%
reactions

# %% [markdown]
# We will experiment with reactions `2` and `4`, which are defined as follows:

# %%
# dictionary representing input data for reaction 2
reactions[2].input_data

# %%
# dictionary representing input data for reaction 4
reactions[4].input_data

# %%
# let's test the rate expression
[reactions[2].rate(T), reactions[4].rate(T)]

# %% [markdown]
# ### Replace Reactions with Custom Reactions
#
# For simple `rate-constant` expressions that are only a function of temperature, `ct.CustomRate` allows for a simple definition of user-defined custom rates.
#
# Let's replace the two reactions with custom rates that are defined by Python `lambda` expressions.

# %%
# replace 'H2 + O <=> H + OH' with equivalent expression
custom2 = ct.Reaction(
    equation='H2 + O <=> H + OH',
    rate=lambda T: 38.7 * T**2.7 * exp(-3150.1542797022735/T))
custom2

# %%
# replace 'H2O2 + O <=> HO2 + OH' with equivalent expression
custom4 = ct.Reaction(
    equation='H2O2 + O <=> HO2 + OH',
    rate=lambda T: 9630.0 * T**2.0 * exp(-2012.8781339950629/T))
custom4

# %%
# let's test the replacement rate expressions
[custom2.rate(T), custom4.rate(T)], [reactions[2].rate(T), reactions[4].rate(T)]

# %%
# assemble a new `Solution` object so things can be tested
reactions[2] = custom2
reactions[4] = custom4
gas1 = ct.Solution(thermo='ideal-gas', kinetics='gas',
                   species=species, reactions=reactions)


# %% [markdown]
# > **Note:** This approach is simple, but cannot be generalized to general reaction rate expressions that may depend on additional properties, for example pressure or composition.

# %% [markdown]
# ### Replace Reactions with Extensible Reactions
#
# Generic reaction rate parameterizations require information that needs explicit handling of both reaction rate itself (via specializations of `ct.ExtensibleRate`) and associated data.
#
# Let's again replace the two reactions with customized alternatives, where we will define a _new reaction rate parameterization_ rather than hand-coding rate parameters as above.

# %% [markdown]
# **1. Data Associated with a NEW Extensible _Arrhenius_ Reaction Rate**
#
# Data used by an extensible reaction needs to be defined as a specializations of `ct.ExtensibleRateData`.

# %%
class ExtensibleArrheniusData(ct.ExtensibleRateData):
    __slots__ = ("T",)
    def __init__(self):
        self.T = None

    def update(self, gas):
        T = gas.T
        if self.T != T:
            self.T = T
            return True
        else:
            return False

# %% [markdown]
# **2. Parameterization of the NEW Extensible _Arrhenius_ Reaction Rate**
#
# Data used by an extensible reaction needs to be defined as a specializations of `ct.ExtensibleRateData`.

# %%
@ct.extension(name="extensible-Arrhenius", data=ExtensibleArrheniusData)
class ExtensibleArrhenius(ct.ExtensibleRate):
    __slots__ = ("A", "b", "Ea_R")
    def set_parameters(self, params, units):
        self.A = params.convert_rate_coeff("A", units)
        self.b = params["b"]
        self.Ea_R = params.convert_activation_energy("Ea", "K")

    def get_parameters(self, params):
        params.set_quantity("A", self.A, self.conversion_units)
        params["b"] = self.b
        params.set_activation_energy("Ea", self.Ea_R, "K")

    def validate(self, equation, soln):
        if self.A < 0:
            raise ValueError(f"Found negative 'A' for reaction {equation}")

    def eval(self, data):
        return self.A * data.T**self.b * exp(-self.Ea_R/data.T)


# %% [markdown]
# **3. Redefine Reactions with NEW Rate Parameterization**
#
# Using a rate parameterization allows for the definition of new reactions similar to standard YAML input files.

# %%
# replace 'H2 + O <=> H + OH' with equivalent extensible expression
extensible_yaml2 = """
    equation: H2 + O <=> H + OH
    type: extensible-Arrhenius
    units: {length: cm, quantity: mol, activation-energy: cal/mol}
    A: 3.87e+04
    b: 2.7
    Ea: 6260.0
    """
extensible2 = ct.Reaction.from_yaml(extensible_yaml2, gas0)
extensible2

# %%
# replace 'H2O2 + O <=> HO2 + OH' with equivalent extensible expression
extensible_yaml4 = """
    equation: H2O2 + O <=> HO2 + OH
    type: extensible-Arrhenius
    units: {length: cm, quantity: mol, activation-energy: cal/mol}
    A: 9.63e+06
    b: 2
    Ea: 4000
    """
extensible4 = ct.Reaction.from_yaml(extensible_yaml4, gas0)
extensible4

# %%
# assemble a new `Solution` object so things can be tested
reactions[2] = extensible2
reactions[4] = extensible4
gas2 = ct.Solution(thermo="ideal-gas", kinetics="gas",
                   species=species, reactions=reactions)


# %% [markdown]
# ### Testing!
#
# Now we have three versions of `Solution` objects:
# * `gas0` ... contains the mechanism with *native* reaction rate parameterizations
# * `gas1` ... two reaction rates are replaced by two hand-coded `ct.CustomRate` objects
# * `gas2` ... the same two rates are replaced using the new `ExtensibleArrhenius` reaction rate parameterization
#
# Further, we need a test case. Let's use a standard ignition calculation.

# %%
def ignition(gas, dT=0):
    """Run ignition simulation"""
    # set up reactor
    gas.TP = T + dT, P
    gas.set_equivalence_ratio(0.8, fuel, 'O2:1.0, N2:3.773')
    r = ct.IdealGasReactor(gas)
    net = ct.ReactorNet([r])
    net.rtol_sensitivity = 2.e-5

    # time reactor integration
    t1 = default_timer()
    net.advance(.5)
    t2 = default_timer()

    return t2 - t1, net.solver_stats['steps']

# %% [markdown]
# **Run Simulations and Output Results**
#
# All we're interested in is speed of calculation.

# %%
repeat = 100
print(f"Average time of {repeat} simulation runs for '{mech}' ({fuel})")

sim0 = 0
sim0_steps = 0
for i in range(repeat):
    elapsed, steps = ignition(gas0, dT=i)
    sim0 += elapsed
    sim0_steps += steps
sim0 *= 1e6 / sim0_steps
print(f'- Built-in rate parameterizations: {sim0:.2f} μs/step (T_final={gas0.T:.2f})')

sim1 = 0
sim1_steps = 0
for i in range(repeat):
    elapsed, steps = ignition(gas1, dT=i)
    sim1 += elapsed
    sim1_steps += steps
sim1 *= 1e6 / sim1_steps
print('- Two Custom reactions: '
      f'{sim1:.2f} μs/step (T_final={gas1.T:.2f}) ... '
      f'{100 * sim1 / sim0 - 100:+.2f}%')

sim2 = 0
sim2_steps = 0
for i in range(repeat):
    elapsed, steps = ignition(gas2, dT=i)
    sim2 += elapsed
    sim2_steps += steps
sim2 *= 1e6 / sim2_steps
print('- Two Extensible reactions: '
      f'{sim2:.2f} μs/step (T_final={gas2.T:.2f}) ... '
      f'{100 * sim2 / sim0 - 100:+.2f}%')

# %%
