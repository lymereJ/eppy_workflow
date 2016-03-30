# EppyWorkflow

## Description
This repository contains a set of Python functions and a master CSV file that can be used as a workflow using [Eppy](https://github.com/santoshphilip/eppy) to create and modify [EnergyPlus](https://github.com/NREL/EnergyPlus) models.

## Why?
I like to use [Eppy](https://github.com/santoshphilip/eppy) to modify [EnergyPlus](https://github.com/NREL/EnergyPlus) models to run parametric studies. I've always been missing a central repository of all the function I have created so I could use the same function on any projects.

## How does it work?
+ Write Python functions using [Eppy](https://github.com/santoshphilip/eppy) 
+ Add these functions to the master CSV files (as shown in the template)
+ Add runs to the master CSV file and for each runs provide the arguments for each function
+ Run the `Main.py` script

Hop'la, you've got yourself modified EnergyPlus models:exclamation:

## Structure

* Root
..* Main.py
..* importdir.py
..* :filefolder: FunctionLibrary
....* Function1.py
....* Function2.py
....* etc...