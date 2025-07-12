import numpy as np
import camb

# speed of light [km/s]
c_kms=2.997e5

def get_cosmology(
    thetastar=None,
    H0=68.0,
    mnu=0.0,
    omch2=0.12,
    ombh2=0.022,
    omk=0.0,
    w=-1,
    wa=0,
):
    """Given set of cosmological parameters, return CAMB cosmology object."""
    pars = camb.CAMBparams()
    # set background cosmology
    pars.set_cosmology(thetastar=thetastar, H0=H0, ombh2=ombh2, omch2=omch2, omk=omk, mnu=mnu)
    # set DE
    pars.set_dark_energy(w=w, wa=wa)
    # compute background quantities
    data = camb.CAMBdata()
    data.calc_background(pars)
    # store both camb pars and data
    cosmo = {'pars':pars, 'data':data}
    return cosmo

def D_H_Mpc(z, cosmo):
    Hz = cosmo['data'].hubble_parameter(z)
    return c_kms / Hz

def D_M_Mpc(z, cosmo):
    D_M = cosmo['data'].angular_diameter_distance(z)*(1+z)
    return D_M

def r_d_Mpc(cosmo):
    # dummy BAO data to extract r_d
    z=1.0
    bao_info = cosmo['data'].get_BAO([z], cosmo['pars'])
    # rs/DV, H, DA, F_AP
    D_A = bao_info[0][2]
    D_M = D_A * (1+z)
    H_z = bao_info[0][1]
    D_H = c_kms / H_z
    D_V = (z * D_M**2 * D_H)**(1/3)
    rd_DV = bao_info[0][0]
    r_d = rd_DV * D_V
    return r_d
