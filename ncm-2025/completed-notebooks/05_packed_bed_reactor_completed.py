# %% [markdown]
# ## Packed bed reactors in Cantera
#
# In this example we simulate a packed bed reactor (PBR) using a series of continuously stirred tank reactors (CSTRs). This technique makes use of the following advanced functionality in Cantera:
#
# 1. Simulating multiphase thermodynamics and reaction mixtures using Cantera
# 2. Using a Cantera reactor network object to work with our two-phase system
#
# The design equation for a PBR is as follows:
#
# $$W_{cat} = F_{A0}\int_{0}^{X} \frac{dX}{-r'_A}$$
#
# and the equation for a fluidized CSTR is:
#
# $$W_{cat} = F_{A0} \frac{F_{A0}X}{-r'_A}$$
#
# Comparing both of these on a Levenspiel plot shows that the limiting case for a large number of CSTRs (with differentially small volumes) in series will yield an approximation of a PBR:
#
# <img src="../images/levenspiel_plot.png"  width="500">

# %%
import cantera as ct

%matplotlib widget
import matplotlib.pyplot as plt

print(f"Using Cantera version: {ct.__version__}")

# %% [markdown]
# ### Cantera Simulation Steps
#
# As usual for a Cantera simulation, there are 3 main steps:
#
# 1. Create the appropriate phases from an input file
# 2. Set the initial conditions for the simulation
# 3. Run the simulation
#
# #### Inputs
#
# To start, we will specify the inputs for the packed bed reactor:
#
# - the reactor dimensions (radius, length, and catalyst bed area)
# - the catalyst properties (surface area to volume ratio)
# - inlet conditions (flowrate, mole fractions)
# - solver specifications (number of CSTRs we will use to approximate a PFR, time step size)

# %%
# Inputs
temp = 700.0           # Temperature (K)
length = 0.3           # Catalyst bed length (m)
area = 1.0e3           # Catalyst bed total area (m^2)
cat_area_per_vol = 10  # Catalyst particle surface area per unit volume (m^2/m^3)
velocity = 0.4         # Gas velocity (m/s)
porosity = 0.3         # Catalyst bed porosity (unitless)

# The PFR will be simulated by a chain of 'NReactors' stirred reactors.
NReactors = 201

# %% [markdown]
# #### Create Cantera phases and set initial conditions
#
# For this problem, we need both a surface phase and a gas phase. Most conveniently, these phase definitions will be in the same input file and the phase can be chosen by specifying the phase name. You will create a gas bulk phase using the `methane_pox_on_pt.yaml` example input file distributed with Cantera. Then, you will create a surface phase from the same input file.
#
# The names of the phases correspond with the `name` field from the YAML input file. For our example, we have 2 phases named `gas` and `Pt_surf`:
#
# ```
# phases:
# - name: gas
#   thermo: ideal-gas
#   # Further input removed for space
# - name: Pt_surf
#   thermo: ideal-surface
#   # Further input removed for space
# ```
#
# First, you will specify the temperature, pressure, and concentrations for the gas phase. Then, specify the temperature and pressure for the surface phase.

# %%
yaml_file = 'methane_pox_on_pt.yaml'

gas = ct.Solution(yaml_file, 'gas')
gas.TPX = temp, ct.one_atm, 'CH4:1, O2:1.5, AR:0.1'

# %% [markdown]
# When creating a `Solution`, the _second_ argument tells Cantera which phase to load from the input file. By default, Cantera chooses the first, but when there are multiple phases present it is good practice to be explicit.
#
# Surface phases are loaded using the `Interface` class. As with the `Solution`, the first and second arguments are the input file name and the phase name, respectively. For an `Interface`, the third argument must be a list of the adjacent bulk phase instances. In this case, we will use the variable `gas`.

# %%
surf = ct.Interface(yaml_file, 'Pt_surf', [gas])
surf.TP = temp, ct.one_atm

# %% [markdown]
# After initializing the gas and surface phases, we next want to calculate the differential volume and the differential length of differential CSTR elements. Additionally, the catalyst area and inlet mass flow rate need to be calculated.

# %%
rlen = length / (NReactors - 1)
rvol = area * rlen * porosity
cat_area = cat_area_per_vol * rvol
mass_flow_rate = velocity * gas.density * area

# %% [markdown]
# #### Creating a chain of CSTRs to approximate a PFR
# The plug flow reactor is represented by a linear chain of zero-dimensional reactors. The gas at the inlet to the first one has the specified inlet composition, and for all others the inlet composition is fixed at the composition of the reactor immediately upstream. Since in a PFR model there is no diffusion, the upstream reactors are not affected by any downstream reactors, and therefore the problem may be solved by simply marching from the first to last reactor, integrating each one to steady state.
#
# <img src="../images/Chain_of_CSTRs.png"  width="700">

# %% [markdown]
# Next, we need to initialize our reactor objects of the type 'IdealGasReactor'. We also need to attach a surface onto it to run all surface reactions simultaneously.

# %%
r = ct.IdealGasReactor(gas, energy='off')
r.volume = rvol

rsurf = ct.ReactorSurface(surf, r, A=cat_area)

# %% [markdown]
# Next, create two reservoirs: one for the supply gas (upstream) and one for the outlet (downstream). To control our material balance across the reactor, we will need to introduce the `MassFlowController` and the `PressureController` objects. The mass flow rate in the `MassFlowController` is constant here.

# %%
upstream = ct.Reservoir(gas, name='upstream')

downstream = ct.Reservoir(gas, name='downstream')

m = ct.MassFlowController(upstream, r, mdot=mass_flow_rate)

v = ct.PressureController(r, downstream, primary=m, K=1e-5)

# %% [markdown]
# We will then create a `ReactorNet` object.

# %%
sim = ct.ReactorNet([r])
sim.max_err_test_fails = 12

# set relative and absolute tolerances on the simulation
sim.rtol = 1.0e-9
sim.atol = 1.0e-21

# %% [markdown]
# We are now ready to run our reactor. We will print the CH4, H2, and CO mile fractions so we can track our progress down the PBR. We will also record our data while the reactor is running.

# %%
print('    distance       X_CH4        X_H2        X_CO')

states = ct.SolutionArray(gas, extra=['distance'])

# run each differential reactor volume element sequentially
for n in range(NReactors):

    # Set the state of the reservoir to match that of the previous reactor.
    gas.TDY = r.thermo.TDY
    upstream.syncState()
    sim.reinitialize()

    # run the CSTR to steady state, since we are getting
    # our steady state concentrations in the PFR
    sim.advance_to_steady_state()
    dist = n * rlen * 1.0e3  # distance in mm

    # generate our solution array using the states object
    states.append(r.thermo.state, distance=dist)

    if n % 10 == 0:
        print('  {0:10f}  {1:10f}  {2:10f}  {3:10f}'.format(
            dist, *gas['CH4', 'H2', 'CO'].X))

# %% [markdown]
# ### Results
#
# Plot the resulting surface coverages and concentrations over the length of the PFR using our `states` solution array

# %%
for i in range(gas.n_species):
    spec = gas.species_names[i]
    plt.plot(states.distance, states.X[:,i],label = spec)
    plt.legend()

plt.xlabel("Distance (mm)")
plt.ylabel("mole fraction")
plt.show()

# %%
