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

Moreover, the following folders will be created at run time to store some of the results:

 - `data/` : forecasted BAO measurements are stored here

 - `runs/` : MCMC chains are stored here


## Cosmological models

The code is ready to fit the parameters of a few cosmological models, and for two different parameterizations (BAO and CMB).

### BAO fits

When fitting only BAO data, we will always use `H_0 r_d` as `Omega_m` as free parameters

 - `lcdm` : 2 free parameters (`H_0 r_d` and `Omega_m`)

 - `olcdm` : 3 free parameters (`H_0 r_d` , `Omega_m` and `Omega_k`)

 - `w0wa` : 4 parameters (`H_0 r_d` , `Omega_m`, `w_0` and `w_a`)

### CMB fits

When fitting only CMB data, or combinations of CMB and BAO data, we will always use instead the 3 free parameters of the compressed CMB likelihood: `theta_star`, `Omega_b h^2` and `Omega_bc h^2` .

 - `lcdm` : 3 free parameters (`theta_star`, `Omega_b h^2` and `Omega_bc h^2`)
   
 - `olcdm` : 4 free parameters (`theta_star`, `Omega_b h^2`, `Omega_bc h^2` and `Omega_k`)

 - `nulcdm` : 4 free parameters (`theta_star`, `Omega_b h^2`, `Omega_bc h^2` and `mnu`)

 - `w0wa` : 5 parameters (`theta_star`, `Omega_b h^2`, `Omega_bc h^2`, `w_0` and `w_a`)


## Create likelihoods

First of all, several paths in the notebooks are hardcoded in the beginning of the notebooks.
These will need to be changed in order for the notebooks to run on your laptop / at NERSC. 
The remaining of the notebook should run once these initial paths have been set.

### Make synthetic BAO likelihoods

There are two notebooks to generate synthetic BAO likelihoods that can later on be used to run chains.

 - `make_desi_data.ipynb` : generates a DESI-Y5 forecast 

 - `make_mock_data.ipynb` : generates toy (not realistic) BAO forecasts at different z

### Compressed CMB likelihood

In order to simplify the analyses, we only use a compressed CMB likelihood that is independent from late-time cosmology. This is a 3D Gaussian likelihood with free parameters: `theta_star`, `Omega_b h^2` and `Omega_bc h^2`. 

In particular we use the implementation used in the DESI DR2 cosmological analysis (https://arxiv.org/abs/2503.14738), itself based on the analysis by Lemos & Lewis (2023, https://arxiv.org/abs/2302.12911).

The details of the implementation can be found under `py/compressed_cmb.py` .


## How to run the basic analyses?

### CMB-only cosmological analyses

Using only the compressed CMB likelihood we can already constraint models with the CMB parameterization. This can be run for instance with the `run_cmb.ipynb` notebook. 

While the LCDM run can be quite fast (15 minutes in a laptop), other models with less constrained parameters can take a while if running on your laptop.

### BAO-only cosmological analyses

Using only BAO likelihoods we can also constraint models with the BAO parameterization. In the notebook `run_bao.ipynb` you can see how to run analyses for the forecasted DESI-Y5 likelihoods, either combined analyses or one tracer at a time (BGS, LRG, ELG, QSO and LYA separately).


