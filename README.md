# EppyWorkflow

## Description
This repository contains a set of Python functions and a master CSV file that can be used as a workflow using [Eppy](https://github.com/santoshphilip/eppy) to create and modify [EnergyPlus](https://github.com/NREL/EnergyPlus) models.

## Why?
I like to use [Eppy](https://github.com/santoshphilip/eppy) to modify [EnergyPlus](https://github.com/NREL/EnergyPlus) models to run parametric simulations. However, I've always been missing a central repository of all the functions that I create for each project. Using this workflow I can reuse any functions that I have created for previous projects.

## How does it work?
+ Write Python functions using [Eppy](https://github.com/santoshphilip/eppy) 
+ Add these functions to the master CSV file
+ Add parametric runs to the master CSV file
+ For each new run provide the corresponding argument for each function
+ Run the `Main.py` script

Hop'la, you've got yourself your modified EnergyPlus models ready for simulation:exclamation:

## Structure

* Root
  * :memo: Main.py
  * :memo: importdir.py
  * :file_folder: FunctionLibrary
    * :memo: Function1.py
    * :memo: Function2.py
    * etc...