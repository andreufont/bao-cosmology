# bao-cosmology

Simple cosmological analysis with BAO measurements


## Installation

At this point there is no installation enabled, and one needs to provide the specific paths to the python modules.
 
### External dependencies

Besides generic python libraries (numpy, sys, yaml, matplotlib, pathlib, subprocess), 
some of the scripts use the following cosmology-specific packages that can be installed via pip:
 - camb
 - getdist
 - cobaya


## Structure

Besides this README file, in the repo you will find the following folders:

 - `py/` : a few python modules used by the notebooks and scripts
 
 - `notebooks/` : examples for how to run the BAO forecasts and the cosmological inference

 - `scripts/` : at this point it only contains the default Cobaya batch script to be used in clusters (like NERSC)

 - `data/` : forecasted BAO measurements are stored here

 - `runs/` : MCMC chains are stored here


## How to run the basic analyses?

First of all, several paths in the notebooks are hardcoded in the beginning of the notebooks.
These will need to be changed in order for the notebooks to run on your laptop / at NERSC. 
The remaining of the notebook should run once these initial paths have been set.


### Make synthetic BAO likelihoods

There are two notebooks to generate synthetic BAO likelihoods that can later on be used to run chains.

 - `make_desi_data.ipynb` : generates a DESI-Y5 forecast 

 - `make_mock_data.ipynb` : generates other, not realistic BAO forecasts at different z that can be useful 


### BAO-only cosmological analyses



