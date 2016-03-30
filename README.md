# EppyWorkflow

## Description
This repository contains a set of Python functions and a master CSV file that can be used as a workflow using [Eppy](https://github.com/santoshphilip/eppy) to create and modify [EnergyPlus](https://github.com/NREL/EnergyPlus) models.

## Why?
I like to use [Eppy](https://github.com/santoshphilip/eppy) to modify [EnergyPlus](https://github.com/NREL/EnergyPlus) models in order to run parametric simulations. However, I've always been missing a central repository containing all the functions that I have created in the past. With this workflow I can reuse any of the functions that I have previously created for any projects.

## How does it work?
+ Write Python functions using [Eppy](https://github.com/santoshphilip/eppy) 
+ Add these functions to the master CSV file
+ Add parametric runs to the master CSV file
+ For each run provide the corresponding argument for each function
+ Run the `Main.py` script

Hop'la, you've got yourself your modified EnergyPlus model(s) ready for simulation:exclamation:

## Structure

* Root
  * :memo: Main.py
  * :memo: importdir.py
  * :file_folder: Functions
    * :memo: Function1.py
    * :memo: Function2.py
    * etc...