# %%
import numpy as np
import matplotlib.pyplot as plt
import cantera as ct
print(ct.__file__)

plt.rcParams['figure.constrained_layout.use'] = True
%matplotlib widget

# %% [markdown]
# ## Mechanism files & basic info
#
# https://github.com/Cantera/cantera/blob/main/data/gri30.yaml

# %%
gas = ct.Solution('gri30.yaml')

# %%
gas.n_species, gas.n_reactions

# %%
print(gas.species_names)

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
CH4 = gas.species("CH4")
CH4.thermo.input_data

# %%
TT = np.linspace(300, 2000, 200)
cp = [CH4.thermo.cp(T) for T in TT]

# %%
fig, ax = plt.subplots()
ax.plot(TT, cp);

# %%
gas()

# %% [markdown]
# ## Setting thermodynamic state
# - Always requires two variables, e.g. $(T, P)$ or $(T, v)$ or $(s, P)$ etc.
# - Specify `None` to hold a property constant
#
# https://cantera.org/documentation/docs-3.0/sphinx/html/cython/thermo.html#thermophase

# %%
gas.TP = 500, ct.one_atm
gas()

# %%
gas.SP = None, 2 * ct.one_atm
gas()

# %%

# %% [markdown]
# ## Setting composition
# - Main ways are by setting either mass fractions ($Y$) or mole fractions ($X$)
# - Can be set alone (in which case $(T,\rho)$ held constant), or with a valid property pair
# - Mass/mole fractions are automatically normalized to 1.0
# - Can also set equivalence ratio

# %%
gas.TPX = 300, ct.one_atm, {'H2': 1.0, 'O2': 1.5}
gas()

# %%
X = np.zeros(gas.n_species)
X[9:14] = 1.0
gas.X = X
gas()

# %%
gas.TPY = None, None, "CH4:1.0, N2:3"
gas()

# %%
gas.TP = 500, 10 * ct.one_atm
gas.set_equivalence_ratio(0.5, "CH4:1.0", "O2:1, N2:3.76")
gas()

# %%
# gas.set_equivalence_ratio?

# %% [markdown]
# ## Flame temperature calculation
#
# With a guest appearance by the `SolutionArray` class.

# %%
phis = np.linspace(0.4, 3.0, 100)
Tad = []
T0 = 300
P0 = ct.one_atm
fuel = "C2H6: 1.0"

for phi in phis:
    gas.TP = T0, P0
    gas.set_equivalence_ratio(phi, fuel, "O2:1.0, N2:3.76")
    gas.equilibrate("HP")
    Tad.append(gas.T)

# %%
fig, ax = plt.subplots()
ax.plot(phis, Tad)
ax.set(xlabel="Equivalence ratio, $\\phi$", ylabel="adiabatic flame temperature [K]");

# %%
states = ct.SolutionArray(gas, len(phis))
states.Y.shape

# %%
states.TP = T0, P0
states.set_equivalence_ratio(phis, fuel, "O2:1.0, N2:3.76")
states.equilibrate("HP")

# %%
fig, ax = plt.subplots()
species = ['CO2', 'CO', 'H2', 'O2']
ax.plot(phis, states(*species).X, label=species)
ax.legend();

# %% [markdown]
# ## Kinetics & Reactions
#
# https://cantera.org/documentation/docs-3.0/sphinx/html/cython/kinetics.html#kinetics

# %%
R = gas.reaction(1)
R

# %%
R.rate.pre_exponential_factor

# %%
R.reactants

# %%
gas.forward_rate_constants[1]

# %%
gas.net_rates_of_progress[1]

# %% [markdown]
# ## Defining reactions & exploring equilibrium
#
# $$ a \mathrm{A} + b \mathrm{B} \rightleftharpoons c \mathrm{C} + d \mathrm{D} $$
#
# $$ \Delta_r^\circ \hat{g} = \Delta_r^\circ \hat{h} - T \Delta_r^\circ \hat{s}$$
#
# $$ K_c = \frac{k_f}{k_r} = \frac{[\mathrm{C}]^c [\mathrm{D}]^d}{[\mathrm{A}]^a [\mathrm{B}]^b} = \exp\left( \frac{\Delta_r^\circ \hat{g}}{RT} \right) \left( \frac{p^o}{RT}\right)^{\nu_{net}} $$

# %%
R1 = ct.Reaction(equation="CO + O = CO2", rate=ct.Arrhenius(0.0, 0.0, 0.0))
R2 = ct.Reaction(equation="H + OH = H2O", rate=ct.Arrhenius(0.0, 0.0, 0.0))
gas.add_reaction(R1)
gas.add_reaction(R2)

# %%
iR1 = gas.n_reactions - 2
iR2 = gas.n_reactions - 1

T = np.linspace(300, 2500, 500)
states = ct.SolutionArray(gas, len(T))
states.TPX = T, ct.one_atm, "CO2:1.0, H2O:1.0, N2:3.76, O2:1.0"
dh0 = states.delta_standard_enthalpy[:, [iR1,iR2]]
ds0 = states.delta_standard_entropy[:, [iR1,iR2]]
Kc = states.equilibrium_constants[:, [iR1,iR2]]
Kc.shape

# %%
fig, ax = plt.subplots(1,2)
ax[0].plot(T, dh0)
ax[1].plot(T, ds0)
ax[0].legend([R1.equation, R2.equation])

# %%
fig, ax = plt.subplots()
ax.semilogy(T, Kc)

# %% [markdown]
# ## NO$_x$ reaction rates

# %%
for i, R in enumerate(gas.reactions()):
    all_species = R.reactants | R.products
    if 'N' in all_species and 'NO' in all_species:
        print(i, R)

# %%
iZ1 = 177
iZ2 = 178
states.equilibrate("TP")

# %%
fig, ax = plt.subplots()
ax.plot(states.T, states.reverse_rates_of_progress[:, 177], label='R1')
ax.plot(states.T, states.forward_rates_of_progress[:, 178], label='R2')
ax.legend();

# %% [markdown]
# ## Well stirred reactor with NOx
#
# <div>
# <center>
# <!-- <img src="attachment:d2223bec-96e3-4f07-8e46-d0450fcd6be5.png", width="400" /> -->
#     <img src="https://raw.githubusercontent.com/Cantera/cantera-jupyter/e738d0ef0fdd212a0b543d6eb2279572b42530a2/reactors/images/stirredReactorCartoon.png" width="400" style="background: white; border:5px solid white"/>
# </center>
# </div>
#
# $$    m \frac{dn_k}{dt} = V \dot{\omega}_k + \sum_{in} \dot{n}_{k, in} - \sum_{out} \dot{n}_{k, out} $$
#
# $$    \left( \sum_k n_k \hat{c}_{p,k} \right) \frac{dT}{dt} =  - \sum \hat{u}_k \dot{n}_k $$

# %%
gas.TPX = 2000, ct.one_atm, "O2:1.0, N2:3.76, H2O:.01"

wsr = ct.IdealGasMoleReactor(gas)
wsr.volume = 0.1
upstream = ct.Reservoir(gas)
downstream = ct.Reservoir(gas)
inlet = ct.MassFlowController(upstream, wsr, mdot=10.0)
outlet = ct.PressureController(wsr, downstream, primary=inlet)
sim = ct.ReactorNet([wsr])

# %%
states = ct.SolutionArray(gas, extra=['t'])
tEnd = 0.01
while sim.time < tEnd:
    sim.step()
    states.append(state=wsr.thermo.state, t=sim.time)

# %%
fig, ax = plt.subplots()
ax.plot(states.t, states('NO').Y, '.-')


# %%
def calc_nox(phi, mdot):
    gas.TP = 300, ct.one_atm
    gas.set_equivalence_ratio(phi, "CH4:1.0", "N2:3.76, O2:1.0")
    Yf_in = gas["CH4"].Y[0]
    upstream = ct.Reservoir(gas)

    gas.equilibrate("HP")
    wsr = ct.IdealGasMoleReactor(gas)
    wsr.volume = 0.1
    downstream = ct.Reservoir(gas)
    inlet = ct.MassFlowController(upstream, wsr, mdot=mdot)
    outlet = ct.PressureController(wsr, downstream, primary=inlet)
    sim = ct.ReactorNet([wsr])

    tEnd = 4.0
    while sim.time < tEnd:
        sim.step()

    return wsr.thermo["NO"].Y[0] / Yf_in


# %%
fig, ax = plt.subplots()

phi_in = np.linspace(0.5, 1.8, 60)
mdot_in = np.logspace(-2, 2, 7)

for mdot in mdot_in:
    NOx = [calc_nox(phi, mdot) for phi in phi_in]
    ax.plot(phi_in, NOx, label=r"$\dot{m} = " + f"{mdot:.2f}$ kg/s")
ax.legend();

# %%
