#usr/bin/env/ python
"""
stats_calcs.py

Author: Lara Tobias-Tarsh (laratt@umich.edu)
Created: 28/06/2024

Module performs statistics calculations for the 
geometrics package which are called in geometrics.py
"""
import warnings
import numpy as np
import scipy


def histogram_bins(length, rule='sqrt') -> int:
    """
    Function calculates the number of histogram bins based on 
    given string for a set of standard rules.

    The valid rules are rice's rule, sturges' rule, square root rule
    [more rules could be added if necessary]

    Parameters
    ----------
    length : int
        length of the distribution data
    rule : str
        string determining the rule to use.
        Valid strings are: 'sqrt', 'sturges', 'rice'

    Returns
    -------
    nbins : int
        number of bins to use in histogram plotting

    """
    if isinstance(rule,int):
        nbins = length
        warnings.warn(f'input for length ({str(rule)}) is integer. Assuming this is number of bins. If not, check your input!')
    elif rule == 'sqrt':
        nbins = np.ceil(np.sqrt(length))
    elif rule == 'rice':
        nbins = 2 * length**(1.0/3.0)
    elif rule == 'sturges':
        nbins = 1.0 + np.log2(length)
    else:
        raise(TypeError(f'Invalid rule: {rule}. Select from sqrt, rice or sturges only.'))
    return nbins


def get_theoretical_dist(data,comp_distribution):
    """
    Function gets a theoretical distribution of a given type
    and returns a fit, an equivalent sampled distribution or
    both, depending on the choice of the user.

    These fits are created in scipy, making this effectively a 
    wrapper for the scipy.rvs method.

    Select from:
        'normal',
        'lognormal',
        'exponenatial',
        'logistic',
        'powerlaw',
        'pareto',
        'genpareto',
        'weibull_min',
        'weibull_max',
        'gumbel_r',
        'gumbel_l',
        'inv_norm',
        'gamma'

    Parameters
    ----------
    data : arrayLike
        array with the data to fit similar distribution to
    comp_distribution : str
        string defining the distribution type

    Returns
    -------
    comp_samples : arrayLike
        distribution drawn from the theoretical distribution
    pdf_fitted : type
        fitted model from the theoretical distribution
    """
    # Dictionary to map distribution names to their corresponding scipy.stats objects
    distributions = {
        'normal': scipy.stats.norm,
        'lognormal' : scipy.stats.lognorm,
        'exponential': scipy.stats.expon,
        'logistic': scipy.stats.logistic,
        'powerlaw' : scipy.stats.powerlaw,
        'pareto': scipy.stats.pareto,
        'genpareto': scipy.stats.genpareto,
        'weibull_min': scipy.stats.weibull_min,
        'weibull_max': scipy.stats.weibull_max,
        'gumbel_r': scipy.stats.gumbel_r,
        'gumbel_l': scipy.stats.gumbel_l,
        'inv_norm' : scipy.stats.invgauss,
        'gamma' : scipy.stats.gamma
    }
    
    dist = distributions.get(comp_distribution.lower())
    if dist is not None:
        try:
            # Fit the distribution to the data
            params = dist.fit(data)

            # Generate random samples from the fitted distribution
            comp_samples = dist.rvs(*params, size=len(data))
            pdf_fitted = dist.pdf(data, *params) * len(data)

                
            # Ensure valid parameters
            if not all(np.isfinite(params)):
                raise ValueError(f"Invalid parameters: {params}")

        except Exception as e:
                print(f"Error fitting {comp_distribution} distribution: {e}")
    
    return comp_samples, pdf_fitted
                