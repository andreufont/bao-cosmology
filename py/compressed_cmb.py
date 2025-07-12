
# mean and covariance from https://github.com/cosmodesi/desi-y3-kp/blob/24c317301256d659f819c4b17cc3ed4a154bf303/desi_y3_cosmo_bindings/cobaya_likelihoods/cmb_likelihoods/CMB_standard_compression_PR4.yaml
all_input_params = ['thetastar', 'ombh2', 'ombch2']
all_means = [0.01041027, 0.02223208, 0.14207901]
all_covs = [[ 6.62099420e-12,  1.24442058e-10, -1.19287532e-09], 
            [ 1.24442058e-10,  2.13441666e-08, -9.40008323e-08], 
            [-1.19287532e-09, -9.40008323e-08,  1.48841714e-06]]

def get_compressed_cmb_likelihood(thetastar=True, ombh2=False, ombch2=False):
    # Cobaya needs these to be in the right order
    input_indices = []
    if thetastar is True:
        input_indices.append(0)
    if ombh2 is True:
        input_indices.append(1)
    if ombch2 is True:
        input_indices.append(2)
    assert len(input_indices)>0, 'we need at least one compressed CMB param'

    # figure out parameter names to be used
    input_params = [all_input_params[i] for i in input_indices]

    # figure out means and covariances to be used 
    means = []
    covs = []
    for i in input_indices:
        means.append(all_means[i])
        cov_row = []
        for j in input_indices:
            cov_row.append(all_covs[i][j])
        covs.append(cov_row)
    
    # prepare dictionary for cobaya
    cmb_like = {'class': 'gaussian_mixture', 
                'means': [means],
                'covs': covs, 
                'input_params': input_params,
                'output_params': []
    }

    return cmb_like


def get_fiducial_thetastar():
    return all_means[0]


def get_fiducial_ombh2():
    return all_means[1]


def get_fiducial_ombch2():
    return all_means[2]

