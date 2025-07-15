import yaml
from pathlib import Path
from subprocess import run


def get_nersc_script_template():
    # if running at NERSC, return default SLURM script
    base_path = Path('/global/cfs/cdirs/desicollab/users/font/bao-cosmology/')
    assert base_path.exists(), 'Are you running at NERSC? ' + str(base_path)
    return base_path / 'scripts/default_cobaya_batch_script.sh'


def get_theory_config():
    #extra theory arguments
    extra_args = {
        'bbn_predictor': 'PArthENoPE_880.2_standard.dat',
        'dark_energy_model': 'ppf',
        'num_massive_neutrinos': 1
    }
    # build theory dictionary
    camb_config = {'extra_args': extra_args}
    theory_config = {'camb': camb_config}
    return theory_config


def get_sampler_config():
    # extra mcmc arguments
    mcmc_config = {
        'Rminus1_stop': 0.01,
        'Rminus1_cl_stop': 0.02,
        'max_tries': 1000
        #'drag': 'false',
        #'oversample_power': 0.4,
        #'proposal_scale': 1.9,
        #'covmat': 'null',
        #'temperature': 1,
        #'seed': 'null'
    }
    sampler_config = {'mcmc': mcmc_config}
    return sampler_config


def get_bao_params_config(model='lcdm'):

    # start with the BAO parameters that are always sampled
    params_config = {
        'hrdrag': {
            'prior': {
                'min': 1.0,
                'max': 10000.0
            },
            'ref': {
                'dist': 'norm',
                'loc': 99.0,
                'scale': 1.0
            },
            'proposal': 1.0,
            'latex': 'hr_\\mathrm{d}'
        },
        'omm': {
            'prior': {
                'min': 0.01,
                'max': 1.0
            },
            'ref': {
                'dist': 'norm',
                'loc': 0.3152,
                'scale': 0.002
            },
            'proposal': 0.001,
            'drop': 'true'
        }
    }

    # free curvature only in 'olcdm'
    if model == 'olcdm':
        params_config['omk'] = {
            'prior': {
                'min': -0.3,
                'max': 0.3
            },
            'ref': {
                'dist': 'norm',
                'loc': 0.0,
                'scale': 0.01
            },
            'proposal': 0.01,
            'latex': '\\Omega_\\mathrm{k}'
        }
    else:
        params_config['omk'] = {
            'value': 0.0,
            'latex': '\\Omega_\\mathrm{k}'
        }

    # free neutrino masses only in 'nulcdm'
    if model == 'nulcdm':
        params_config['mnu'] = {
            'prior': {
                'min': 0.0,
                'max': 5.0
            },
            'ref': {
                'dist': 'norm',
                'loc': 0.06,
                'scale': 0.01
            },
            'proposal': 0.01,
            'latex': '\\sum m_\\nu'
        }
    else:
        params_config['mnu'] = {
            'value': 0.06,
            'latex': '\\sum m_\\nu'
        }

    # free DE eof only in 'w0wa'
    if model == 'w0wa':
        params_config['w'] = {
            'prior': {
                'min': -3.0,
                'max': 1.0
            },
            'ref': {
                'dist': 'norm',
                'loc': -1.0,
                'scale': 0.02
            },
            'proposal': 0.02,
            'latex': 'w_{0}'
        }
        params_config['wa'] = {
            'prior': {
                'min': -3.0,
                'max': 2.0
            },
            'ref': {
                'dist': 'norm',
                'loc': 0.0,
                'scale': 0.05
            },
            'proposal': 0.05,
            'latex': 'w_{a}'
        }
    else:
        params_config['w'] = {
            'value': -1.0,
            'latex': 'w_{0}'
        }
        params_config['wa'] = {
            'value': 0.0,
            'latex': 'w_{a}'
        }

    # add other parameters that are always fixed (for convenience)
    params_config['H0'] = {
        'latex': 'H_0',
        'value': 68.0
    }
    params_config['ombh2'] = {
        'latex': '\\Omega_\\mathrm{b} h^2',
        'value': 0.0222
    }
    params_config['nnu'] = {
        'latex': 'N_\\mathrm{eff}',
        'value': 3.044
    }

    # derived parameters to link BAO parameters to physical densities
    params_config['omch2'] = {
        'latex': '\\Omega_\\mathrm{c} h^2',
        'value': 'lambda omm, mnu, ombh2, H0: omm*(H0/100)**2 - mnu / 93.14 - ombh2'
    }
    params_config['rdrag'] = {
        'latex': 'r_\\mathrm{d}',
        'value': 'lambda hrdrag, H0: 100 * hrdrag / H0'
    }
    params_config['H0rdrag'] = {
        'latex': 'H_0 r_\\mathrm{d}',
        'derived': 'lambda H0, rdrag: H0 * rdrag'
    }
    params_config['omegamh2'] = {
        'latex': '\\Omega_\\mathrm{m} h^2',
        'derived': 'lambda omegam, H0: omegam*(H0/100)**2'
    }

    # derived parameters that are set by CAMB, and used in other analyses
    params_config['omegam'] = { 'latex': '\\Omega_\\mathrm{m}' }
    params_config['omegal'] = { 'latex': '\\Omega_\\Lambda' }
    params_config['thetastar'] = { 'latex': '\\theta_\\mathrm{s}' }

    return params_config
