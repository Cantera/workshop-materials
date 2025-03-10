---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
print(ct.__file__)

plt.rcParams['figure.constrained_layout.use'] = True
%matplotlib widget
```

## Mechanism files & basic info

https://github.com/Cantera/cantera/blob/main/data/gri30.yaml

```{code-cell} ipython3
gas = ct.Solution('gri30.yaml')
```

```{code-cell} ipython3
gas.n_species, gas.n_reactions
```

```{code-cell} ipython3
print(gas.species_names)
```

## Species thermo data

NASA 7-coefficient polynomials:

$$   \frac{\hat{c}_p^\circ(T)}{\overline{R}} = a_0 + a_1 T + a_2 T^2 + a_3 T^3 + a_4 T^4 $$

$$   \frac{\hat{h}^\circ (T)}{\overline{R} T} = a_0 + \frac{a_1}{2} T + \frac{a_2}{3} T^2 +
                         \frac{a_3}{4} T^3 + \frac{a_4}{5} T^4 + \frac{a_5}{T} $$

$$   \frac{\hat{s}^\circ(T)}{\overline{R}} = a_0 \ln T + a_1 T + \frac{a_2}{2} T^2 + \frac{a_3}{3} T^3 +
                      \frac{a_4}{4} T^4 + a_6 $$

```{code-cell} ipython3
CH4 = gas.species("CH4")
CH4.thermo.input_data
```

```{code-cell} ipython3
TT = np.linspace(300, 2000, 200)
cp = [CH4.thermo.cp(T) for T in TT]
```

```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(TT, cp);
```

```{code-cell} ipython3
gas()
```

## Setting thermodynamic state
- Always requires two variables, e.g. $(T, P)$ or $(T, v)$ or $(s, P)$ etc.
- Specify `None` to hold a property constant

https://cantera.org/documentation/docs-3.0/sphinx/html/cython/thermo.html#thermophase

```{code-cell} ipython3
gas.TP = 500, ct.one_atm
gas()
```

```{code-cell} ipython3
gas.SP = None, 2 * ct.one_atm
gas()
```

```{code-cell} ipython3

```

## Setting composition
- Main ways are by setting either mass fractions ($Y$) or mole fractions ($X$)
- Can be set alone (in which case $(T,\rho)$ held constant), or with a valid property pair
- Mass/mole fractions are automatically normalized to 1.0
- Can also set equivalence ratio

```{code-cell} ipython3
gas.TPX = 300, ct.one_atm, {'H2': 1.0, 'O2': 1.5}
gas()
```

```{code-cell} ipython3
X = np.zeros(gas.n_species)
X[9:14] = 1.0
gas.X = X
gas()
```

```{code-cell} ipython3
gas.TPY = None, None, "CH4:1.0, N2:3"
gas()
```

```{code-cell} ipython3
gas.TP = 500, 10 * ct.one_atm
gas.set_equivalence_ratio(0.5, "CH4:1.0", "O2:1, N2:3.76")
gas()
```

```{code-cell} ipython3
gas.set_equivalence_ratio?
```

## Flame temperature calculation

With a guest appearance by the `SolutionArray` class.

```{code-cell} ipython3
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
```

```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(phis, Tad)
ax.set(xlabel="Equivalence ratio, $\\phi$", ylabel="adiabatic flame temperature [K]");
```

```{code-cell} ipython3
states = ct.SolutionArray(gas, len(phis))
states.Y.shape
```

```{code-cell} ipython3
states.TP = T0, P0
states.set_equivalence_ratio(phis, fuel, "O2:1.0, N2:3.76")
states.equilibrate("HP")
```

```{code-cell} ipython3
fig, ax = plt.subplots()
species = ['CO2', 'CO', 'H2', 'O2']
ax.plot(phis, states(*species).X, label=species)
ax.legend();
```

## Kinetics & Reactions

https://cantera.org/documentation/docs-3.0/sphinx/html/cython/kinetics.html#kinetics

```{code-cell} ipython3
R = gas.reaction(1)
R
```

```{code-cell} ipython3
R.rate.pre_exponential_factor
```

```{code-cell} ipython3
R.reactants
```

```{code-cell} ipython3
gas.forward_rate_constants[1]
```

```{code-cell} ipython3
gas.net_rates_of_progress[1]
```

## Defining reactions & exploring equilibrium

$$ a \mathrm{A} + b \mathrm{B} \rightleftharpoons c \mathrm{C} + d \mathrm{D} $$

$$ \Delta_r^\circ \hat{g} = \Delta_r^\circ \hat{h} - T \Delta_r^\circ \hat{s}$$

$$ K_c = \frac{k_f}{k_r} = \frac{[\mathrm{C}]^c [\mathrm{D}]^d}{[\mathrm{A}]^a [\mathrm{B}]^b} = \exp\left( \frac{\Delta_r^\circ \hat{g}}{RT} \right) \left( \frac{p^o}{RT}\right)^{\nu_{net}} $$

```{code-cell} ipython3
R1 = ct.Reaction(equation="CO + O = CO2", rate=ct.Arrhenius(0.0, 0.0, 0.0))
R2 = ct.Reaction(equation="H + OH = H2O", rate=ct.Arrhenius(0.0, 0.0, 0.0))
gas.add_reaction(R1)
gas.add_reaction(R2)
```

```{code-cell} ipython3
iR1 = gas.n_reactions - 2
iR2 = gas.n_reactions - 1

T = np.linspace(300, 2500, 500)
states = ct.SolutionArray(gas, len(T))
states.TPX = T, ct.one_atm, "CO2:1.0, H2O:1.0, N2:3.76, O2:1.0"
dh0 = states.delta_standard_enthalpy[:, [iR1,iR2]]
ds0 = states.delta_standard_entropy[:, [iR1,iR2]]
Kc = states.equilibrium_constants[:, [iR1,iR2]]
Kc.shape
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,2)
ax[0].plot(T, dh0)
ax[1].plot(T, ds0)
```

```{code-cell} ipython3
fig, ax = plt.subplots()
ax.semilogy(T, Kc)
```

## NO$_x$ reaction rates

```{code-cell} ipython3
for i, R in enumerate(gas.reactions()):
    all_species = R.reactants | R.products
    if 'N' in all_species and 'NO' in all_species:
        print(i, R)
```

```{code-cell} ipython3
iZ1 = 177
iZ2 = 178
states.equilibrate("TP")
```

```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(states.T, states.reverse_rates_of_progress[:, 177], label='R1')
ax.plot(states.T, states.forward_rates_of_progress[:, 178], label='R2')
ax.legend();
```

## Well stirred reactor with NOx

<div>
<center>
<!-- <img src="attachment:d2223bec-96e3-4f07-8e46-d0450fcd6be5.png", width="400" /> -->
    <img src="https://raw.githubusercontent.com/Cantera/cantera-jupyter/e738d0ef0fdd212a0b543d6eb2279572b42530a2/reactors/images/stirredReactorCartoon.png" width="400" />
</center>
</div>

$$    m \frac{dn_k}{dt} = V \dot{\omega}_k + \sum_{in} \dot{n}_{k, in} - \sum_{out} \dot{n}_{k, out} $$

$$    \left( \sum_k n_k \hat{c}_{p,k} \right) \frac{dT}{dt} =  - \sum \hat{u}_k \dot{n}_k $$

```{code-cell} ipython3
gas.TPX = 2000, ct.one_atm, "O2:1.0, N2:3.76, H2O:.01"

wsr = ct.IdealGasMoleReactor(gas)
wsr.volume = 0.1
upstream = ct.Reservoir(gas)
downstream = ct.Reservoir(gas)
inlet = ct.MassFlowController(upstream, wsr, mdot=10.0)
outlet = ct.PressureController(wsr, downstream, primary=inlet)
sim = ct.ReactorNet([wsr])
```

```{code-cell} ipython3
states = ct.SolutionArray(gas, extra=['t'])
tEnd = 0.01
while sim.time < tEnd:
    sim.step()
    states.append(state=wsr.thermo.state, t=sim.time)
```

```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(states.t, states('NO').Y, '.-')
```

```{code-cell} ipython3
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
```

```{code-cell} ipython3
fig, ax = plt.subplots()

phi_in = np.linspace(0.5, 1.8, 60)
mdot_in = np.logspace(-2, 2, 7)

for mdot in mdot_in:
    NOx = [calc_nox(phi, mdot) for phi in phi_in]
    ax.plot(phi_in, NOx, label=r"$\dot{m} = " + f"{mdot:.2f}$ kg/s")
ax.legend();
```

```{code-cell} ipython3

```
