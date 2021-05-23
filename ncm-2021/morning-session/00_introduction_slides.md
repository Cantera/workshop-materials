% 2021 US National Combustion Meeting Cantera Workshop
% May 23, 2021

# Agenda

## Morning Session - Getting Started with Cantera

* General Information
    1. Community Resources
    2. Installation options
    3. Where to find examples
* Adiabatic Flame Temperature Calculations

# Agenda

## Afternoon Session - Parallel Tracks

1. Using Cantera: Ignition Delays, Flame Speeds, and Other Applications
2. Afternoon: Bring Your Own Model: Using Cantera With Your Own Equations
3. Afternoon: Getting Started With Contributing To Cantera

# Overview of Cantera

* Property Calculator
  * Set state of your phase object(s)
  * Evaluate individual properties via function calls.
* Canonical Simulations
  * Cantera comes pre-packaged with a number of simulation tools and examples for a limited set of classic problems
    * 0-D reactors
    * 1-D flames, flows, and reactors
  * These models take user inputs for intial/inlet conditions, reactor geometry, etc.
  * The model sets the state of Cantera objects and evaluating properties to provide terms required to solve/integrate conservation equations.

# Overview of Cantera

* Property evaluation for in-house simulation code
  * For more complex or novel simulations, the user writes their own simulation code.
    * Establishes a solution vector to describe the system state
    * Defines and codes conservation equations
    * Writes calls to Cantera to evaluate terms in the conservation equations

# Application Areas

![Apps.png](./images/Apps.png)

---

* Cantera can be used in a wide variety of applications
  * Combustion
  * Electrochemistry
  * Surface chemistry
  * Non-ideal equations of state
* Cantera's strength is that it is (relatively) easy to add new functionality

# Examples

* Examples are available from the Cantera documentation in several formats
  * Python scripts: <https://cantera.org/examples/python>
  * Jupyter Notebooks: <https://cantera.org/examples/jupyter>
  * Matlab scripts: <https://cantera.org/examples/matlab>
  * C++: <https://cantera.org/examples/cxx>
  * Fortran: <https://cantera.org/examples/fortran>

# Community Resources

* Google Group <https://groups.google.com/forum/#!forum/cantera-users>
  * Email questions to the whole user group
  * The developers watch this group pretty consistently
  * New posters' messages are moderated
  * Messages asking for help with code or error messages must include
    * The code and error message in the post itself (no images please)
    * Any CTI files required to run the code
    * The OS, interface, and version of Cantera you're using

# Community Resources

* Documentation at <https://cantera.org/documentation>
* Has examples and API documentation

# Community Resources

* Cantera source code is on GitHub
* <https://github.com/Cantera/cantera>
* File bug reports (please be detailed and specific)
* Create pull requests to merge your new code

# Community Resources

* Cantera is a fiscally-sponsored project under NumFOCUS
* NumFOCUS is a non-profit umbrella organization that provides support for open-source scientific software
* We would really appreciate your support for Cantera!

[![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://numfocus.salsalabs.org/donate-to-cantera/index.html)

* Plus, we have really cool shirts, mugs, hats, water bottles, onesies, and more!

<img src='https://chart.googleapis.com/chart?cht=qr&chl=https%3A%2F%2Fshop.spreadshirt.com%2Fnumfocus%2Fcantera%2Bofficial%2Blogo%3Fq%3DI1019678777&chs=300x300&choe=UTF-8&chld=L|2' alt='Donate to Cantera!'>
