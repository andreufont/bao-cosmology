from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
from getdist import plots, loadMCSamples


def get_model_label(model):
    if model == 'lcdm':
        model_label = r'$\Lambda$CDM'
    elif model == 'olcdm':
        model_label = r'o$\Lambda$CDM'
    elif model == 'nulcdm':
        model_label = r'$\nu\Lambda$CDM'
    else:
        raise ValueError
    return model_label


def get_chain(chain_path, ignore_rows=0.2):
    samples=loadMCSamples(str(chain_path / 'chain'), settings={'ignore_rows':ignore_rows})
    # add alternative normalization of BAO (from LoVerde & Weiner 2024)
    p = samples.getParams()
    samples.addDerived(p.omegam*(p.H0rdrag/100/147.1)**2, name='ommh2rd2',
                    label=r'\Omega_m h^2 (r_\mathrm{d}/147.1)^2')
    return samples


def get_samples(chains, labels):
    samples = []
    for label in labels:
        samples.append(chains[label])
        #samples.append(chains[label]['samples'])
    return samples


def plot_contours(chains, chain_labels, params, plot_labels=None, width_inch=8):
    # option to pass LaTeX labels for plots
    if plot_labels is None:
        plot_labels = chain_labels
    else:
        assert len(plot_labels)==len(chain_labels)

    # collect samples from chains
    samples=get_samples(chains, chain_labels)
    g = plots.get_single_plotter(width_inch=width_inch)
    if len(params)==2:
        g.plot_2d(samples, params)
        g.add_legend(legend_labels=plot_labels, legend_loc='lower left')
        # specify axes
        ax = g.get_axes()
        #ax.set_xlabel(r'$H_0 r_\mathrm{d}$ [$\mathrm{km}$ $\mathrm{s}^{-1}$]')
        #ax.set_ylabel(r'$\Omega_\mathrm{m}$')
        ax.tick_params(axis='both', which='major', labelsize=g.settings.axes_fontsize)
        #ax.set_ylim(0.25, 0.38)
        #ax.set_xlim(9500, 10500)
    else:
        g.triangle_plot(samples,params, legend_labels=plot_labels, legend_loc="upper right")
        ax = g.get_axes()

    return g, ax
