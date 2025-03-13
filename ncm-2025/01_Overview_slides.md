# Welcome!

## Jupyter Notebooks

The examples are available at https://github.com/Cantera/workshop-materials/tree/acs-2022

# 2025 National Combustion Meeting | Cantera Workshop
## March 16th, 2025
## Richard West, Raymond Speth

# Agenda

| Start Time (EST) | End Time | Session      |
|------------------|----------|--------------|
| 9:00  | 12:00 | Introduction & Tutorials (including a break) |
| 12:00 | 13:30 | *Lunch break (not provided)*           |
| 13:30 | 14:30 | Lighting Talks (contributions welcome)  |
| 14:30 | 15:00 | Contributing to Cantera                      |
| 15:00 | 15:30 | *Break*       |
| 15:30 | 18:00 | What's new in Cantera (including a break)  |

# Overview of Cantera

![CanteraOverview.png](images/CanteraOverview.png)

## Property Calculator

  * Set state of your phase object(s)
  * Evaluate individual properties via function calls.

## "Canonical Simulations"

  * Cantera comes pre-packaged with a number of simulation tools and examples for a limited set of 'classic' problems.
      * 0-D reactors
      * 1-D flames, flows, and reactors
  * These models take user inputs for intial/inlet conditions, reactor geometry, etc.
  * The model sets the state of Cantera objects and evaluating properties to provide terms required to solve/integrate conservation equations.

## Property evaluation for in-house simulation code

  * For more complex or novel simulations, the user writes their own simulation code.
      * Establishes a solution vector to describe the system state
      * Defines and codes conservation equations
      * Writes calls to Cantera to evaluate terms in the conservation equations

# Application Areas

![Apps.png](images/Apps.png)

* Cantera can be used in a wide variety of applications
  * Combustion
  * Electrochemistry
  * Surface chemistry
  * Non-ideal equations of state

* Cantera's strength is that it is (relatively) easy to add new functionality

# Installation

Installation options are provided on the website: https://cantera.org/install/

## Python

- Easiest pathway is via Conda
```
conda create --name ct-env --channel conda-forge cantera ipython matplotlib jupyter
```
(to make an environment called `ct-env` (you can choose whatever environment name you want, though). Then in a python command window, type
```
conda activate ct-env
```
and you can begin using Cantera!
- Can now also install via `pip`

## Other approaches

- Ubuntu users can install the cantera-python3 package from the Cantera PPA.
- Fedora / Enterprise Linux users can install python3-cantera using dnf.
- OpenSUSE users can install packages using zypper.
- Gentoo users can install using emerge.
- FreeBSD users can install using pkg.
- If you want to use the current development version, or add features of your own, you should compile Cantera from source.

# Examples!

* Examples are available from the Cantera documentation in several formats: https://cantera.org/examples/index.html
  * Python scripts: https://cantera.org/examples/python/index.html
  * Jupyter Notebooks: https://cantera.org/examples/jupyter/index.html
  * Matlab scripts: https://cantera.org/examples/matlab/index.html
  * Simple C++ examples: https://cantera.org/tutorials/cxx-guide/simple-example.html

# Community Resources

## Google Group

Link: https://groups.google.com/forum/#!forum/cantera-users
  * Email questions to the whole user group
  * The developers watch this group pretty consistently
  * New posters' messages are moderated
  * Messages asking for help with code or error messages must include
    * The code and error message in the post itself (no images!)
    * Any YAML files required to run the code
    * The OS, interface, and version of Cantera you're using

## Documentation

* Documentation at https://cantera.org/documentation
* Has examples and API documentation (we'll come back to this later)

## GitHub

* Cantera source code is on GitHub
* https://github.com/Cantera/cantera
* File bug reports (please be detailed and specific)
* Create pull requests to merge your new code

## Other

* Cantera is a fiscally-sponsored project under NumFOCUS
* NumFOCUS is a non-profit umbrella organization that provides support for open-source scientific software
* We would really appreciate your support for Cantera!
[![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://numfocus.salsalabs.org/donate-to-cantera/index.html)
* Plus, we have really cool shirts, mugs, hats, water bottles, onesies, and more!
<img src='https://chart.googleapis.com/chart?cht=qr&chl=https%3A%2F%2Fshop.spreadshirt.com%2Fnumfocus%2Fcantera%2Bofficial%2Blogo%3Fq%3DI1019678777&chs=300x300&choe=UTF-8&chld=L|2' alt='Donate to Cantera!'>
