import sys
import numpy as np
from pathlib import Path

# add local modules
import camb_cosmo


def get_BGS_data():
    zs = np.array([0.05,0.15,0.25,0.35])
    sigt = 0.01*np.array([6.65, 2.57, 1.64, 1.37])
    sigp = 0.01*np.array([13.92, 5.40, 3.41, 2.70])
    data = {'zs': zs, 'sig_at': sigt, 'sig_ap': sigp}
    return data


def get_LRG_data():
    zs = np.array([0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05])
    sigt = 0.01*np.array([1.25, 1.05, 0.92, 0.84, 0.78, 0.87, 1.25])
    sigp = 0.01*np.array([2.38, 1.99, 1.74, 1.56, 1.44, 1.52, 2.04])
    data = {'zs': zs, 'sig_at': sigt, 'sig_ap': sigp}
    return data


def get_ELG_data():
    zs = np.array([1.15, 1.25, 1.35, 1.45, 1.55])
    sigt = 0.01*np.array([1.24, 1.26, 1.30, 1.37, 1.87])
    sigp = 0.01*np.array([1.80, 1.80, 1.82, 1.89, 2.46])
    data = {'zs': zs, 'sig_at': sigt, 'sig_ap': sigp}
    return data


def get_QSO_data():
    zs = np.array([1.65, 1.75, 1.85, 1.95, 2.05])
    sigt = 0.01*np.array([3.39, 3.48, 3.67, 3.83, 4.22])
    sigp = 0.01*np.array([4.76, 4.87, 5.14, 5.36, 5.90])
    data = {'zs': zs, 'sig_at': sigt, 'sig_ap': sigp}
    return data


def get_LYA_data():
    zs = np.array([2.15, 2.25, 2.35, 2.45, 2.55, 2.65, 2.75, 2.85, 2.95, 3.05, 3.15, 3.25, 3.35, 3.45])
    sigt = 0.01*np.array([2.02, 2.14, 2.33, 2.56, 2.90, 3.38, 3.95, 4.69, 5.59, 6.73, 8.47, 10.73, 14.48, 19.92])
    sigp = 0.01*np.array([2.16, 2.24, 2.36, 2.52, 2.77, 3.11, 3.50, 4.05, 4.71, 5.51, 6.78, 8.41, 11.1, 14.8])
    data = {'zs': zs, 'sig_at': sigt, 'sig_ap': sigp}
    return data


def get_mock_data(z, sig_at, sig_ap):
    data = {'zs': np.array([z]), 'sig_at': np.array([sig_at]), 'sig_ap': np.array([sig_ap])}
    return data


def write_BAO_files(bao_data, output_path, cosmo, label='BAO'):
    zs = bao_data['zs']
    Nz = len(zs)
    # distances from fiducial cosmology
    DHs = camb_cosmo.D_H_Mpc(zs, cosmo)
    DMs = camb_cosmo.D_M_Mpc(zs, cosmo)
    rd = camb_cosmo.r_d_Mpc(cosmo)
    # relative errors per redshift
    sig_at = bao_data['sig_at']
    sig_ap = bao_data['sig_ap']
    # correlation coefficient
    rho = -0.45

    # specify filenames
    fname_mean = output_path / (label + '_mean.txt')
    fname_cov = output_path / (label + '_cov.txt')
    
    # write BAO means, for each redshift
    with open(fname_mean, 'w') as f:
        f.write('# [z] [value at z] [quantity] \n')
        for iz in range(Nz):
            z = zs[iz]
            # compute means and write to file
            DH_rd = DHs[iz] / rd
            DM_rd = DMs[iz] / rd
            f.write(f'{z} {DH_rd:.4e} DH_over_rs \n')
            f.write(f'{z} {DM_rd:.4e} DM_over_rs \n')

    # write BAO covariance, for each redshift
    with open(fname_cov, 'w') as f:
        for iz in range(Nz):
            z = zs[iz]
            DH_rd = DHs[iz] / rd
            DM_rd = DMs[iz] / rd
            sig_DH_rd = DH_rd * sig_ap[iz]
            sig_DM_rd = DM_rd * sig_at[iz]
            # build covariance block
            C_HH = sig_DH_rd**2
            C_MM = sig_DM_rd**2
            C_HM = sig_DH_rd * sig_DM_rd * rho
            # write covariance block
            cov_row = np.zeros(2*Nz)
            cov_row[2*iz] = C_HH
            cov_row[2*iz+1] = C_HM
            cov_row_str=' '.join(f'{x:.4e}' for x in cov_row)
            f.write(f'{cov_row_str} \n')
            cov_row = np.zeros(2*Nz)
            cov_row[2*iz] = C_HM
            cov_row[2*iz+1] = C_MM
            cov_row_str=' '.join(f'{x:.4e}' for x in cov_row)
            f.write(f'{cov_row_str} \n')


