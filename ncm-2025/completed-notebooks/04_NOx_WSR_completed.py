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
import numpy as np
import matplotlib.pyplot as plt
import cantera as ct
print(ct.__file__)

plt.rcParams['figure.constrained_layout.use'] = True
# %matplotlib widget

# %%
gas = ct.Solution('gri30.yaml')
T = np.linspace(300, 2500, 500)
states = ct.SolutionArray(gas, len(T))
states.TPX = T, ct.one_atm, "CO2:1.0, H2O:1.0, N2:3.76, O2:1.0"

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
ax.plot(states.T, states.reverse_rates_of_progress[:, iZ1], label='R1')
ax.plot(states.T, states.forward_rates_of_progress[:, iZ2], label='R2')
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
gas.TPX = 1900, ct.one_atm, "O2:1.0, N2:3.76, H2O:.01"

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
