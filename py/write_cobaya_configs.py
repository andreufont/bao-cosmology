from pathlib import Path
import yaml
import subprocess
import cobaya

# local module to handle defaults
import cobaya_defaults


def my_mkdir(dir_path):
    dir_path.mkdir(parents=True, exist_ok=True)


def read_yaml(file):
    with open(file, 'r') as file:
        content = yaml.safe_load(file)
    return content


def write_yaml(content, path):
    with open(path, 'w') as file:
        yaml.dump(content, file, sort_keys=False)


def get_bao_like_config(label, data_path):
    fname_mean = (data_path / (label + '_mean.txt')).resolve()
    fname_cov = (data_path / (label + '_cov.txt')).resolve()
    config = {
        'class': 'bao.generic',
        'measurements_file': str(fname_mean),
        'cov_file': str(fname_cov)
    }
    return config


def get_bao_like_configs(labels, data_path):
    config = {}
    for label in labels:
        config[label] = get_bao_like_config(label, data_path)
    return config


def write_multiple_bao_config(model, run_label, bao_labels, data_path, runs_path):
    """ Write a configuration file for Cobaya, given model and BAO data """

    config = {}
    config['theory'] = cobaya_defaults.get_theory_config()
    config['sampler'] = cobaya_defaults.get_sampler_config()
    config['params'] = cobaya_defaults.get_bao_params_config(model=model)

    # setup BAO configuration
    bao_likes = get_bao_like_configs(labels=bao_labels, data_path=data_path)
    config['likelihood'] = bao_likes
        
    # path to chains
    run_path = (runs_path / 'bao' / model / run_label).resolve()
    my_mkdir(run_path)
    config['output'] = str(run_path / 'chain')

    # store config file
    config_file = run_path / 'cobaya_config.yaml'
    write_yaml(config, config_file)
    print('wrote cobaya config file', config_file)

    return config_file



def write_single_bao_config(model, label, data_path, runs_path):
    """ Write a configuration file for Cobaya, given model and BAO data """

    config = {}
    config['theory'] = cobaya_defaults.get_theory_config()
    config['sampler'] = cobaya_defaults.get_sampler_config()
    config['params'] = cobaya_defaults.get_bao_params_config(model=model)

    # setup BAO configuration
    bao_like = get_bao_like_config(label=label, data_path=data_path)
    config['likelihood'] = {label: bao_like}
        
    # path to chains
    run_path = (runs_path / 'bao' / model / label).resolve()
    my_mkdir(run_path)
    config['output'] = str(run_path / 'chain')

    # store config file
    config_file = run_path / 'cobaya_config.yaml'
    write_yaml(config, config_file)
    print('wrote cobaya config file', config_file)

    return config_file


def run_cobaya(config_file, force=False, resume=False):
    config = read_yaml(config_file)
    updated_info, sampler = cobaya.run(config, force=force, resume=resume)
    return updated_info, sampler


def send_cobaya_job(config_file, debug=True, submit=False):

    # figure out Cobaya template script at NERSC
    job_template = cobaya_defaults.get_nersc_script_template()

    # directory from where we will run Cobaya
    run_dir = Path(config_file).parent.resolve()
    command = f'cd {run_dir}\n'

    command += f'cobaya-run-job {config_file}'
    command += f' --nodes 1 --job-template {job_template}'
    if debug:
        command += ' --queue debug --walltime 00:30:00'
    else:
        command += ' --queue regular --walltime 02:00:00'

    if submit:
        process = subprocess.run(command, shell=True, capture_output=False)

    return command

