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

#############
## GLOBALS ##
#############

# Dictionary to map distribution names to their corresponding scipy.stats objects
common_distributions = {
    'normal': scipy.stats.norm,
    'lognormal' : scipy.stats.lognorm,
    'exponential': scipy.stats.expon,
    'logistic': scipy.stats.logistic,
    'powerlaw' : scipy.stats.powerlaw,
    'pareto': scipy.stats.pareto,
    'genpareto': scipy.stats.genpareto,
    'weibull min': scipy.stats.weibull_min,
    'weibull max': scipy.stats.weibull_max,
    'gumbel right': scipy.stats.gumbel_r,
    'gumbel left': scipy.stats.gumbel_l,
    'inverse normal' : scipy.stats.invgauss,
    'gamma' : scipy.stats.gamma
}

#########################################################################################################################

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


def get_theoretical_dist(data,comp_distribution,distributions=common_distributions):
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
        'weibull min',
        'weibull max',
        'gumbel right',
        'gumbel left',
        'inverse normal',
        'gamma'

    Parameters
    ----------
    data : arrayLike
        array with the data to fit similar distribution to
    comp_distribution : str
        string defining the distribution type
    distributions : dict
        dictionary containing key value pairs of the
        distributions common in scipy

    Returns
    -------
    comp_samples : arrayLike
        distribution drawn from the theoretical distribution
    pdf_fitted : type
        fitted model from the theoretical distribution
    """
    
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

def find_best_fit(data,distributions=common_distributions,gen_samples=False,alpha=0.05):
    """
    Function tries to find the ideal fit for a distribution
    from a number of theoretical distributions common in the
    geosciences.

    The simple version of this function uses ONLY the Kolmogorov-Smirnov
    test, but a more complex set of tests will be added later also using
    the Cramer Von-Misses test and Anderson-Darling test.

    note: updates to this function should allow for a user supplied
    distribution

    Parameters
    ----------
    data : arrayLike
        array containing the data to be fitted to
    distributions : dict
        dictionary containing key value pairs of the
        distributions common in scipy
    gen_samples : bool
        specify whether to fit the best theoretical distribution
        and return an equally sized sample
    alpha : float
        significance level to solve at
    
    Returns
    -------
    dist_results : dict
        dictionary with each distribution and their P-Value
    best_theor_dist : arrayLike
        best theoretical distribution for the data
    """
    # set dictionary to store results
    dist_results = {}
    # check if there is a better way for this to be done
    best_stat = None
    best_pval = None
    best_dist = None
    

    # loop through the key value pairs in the distribution and test
    for dist_name, val in zip(distributions.keys(),distributions.values()):
        # fit a distribution
        samples, theor_dist = get_theoretical_dist(data,dist_name)
        # perform K-S test with sampled distribution
        ks_stat, pval = scipy.stats.ks_2samp(data, samples)
        ks_stat = round(ks_stat,2)
        # store results in dictionary
        dist_results[dist_name] = (ks_stat,pval)

        # if there is no best distribution, store the results immediately
        if best_dist is None:
            best_dist = dist_name
            best_stat = ks_stat
            best_pval = pval
        
        # if the best P-Value is not statistically significant
        elif best_pval > alpha:
            # replace if best the test statistic is larger the current one
            if best_stat > ks_stat:
                best_stat = ks_stat
                best_dist = dist_name
                best_pval = pval

        # if the best P-Value is statistically significant    
        else:
            # replace if the current data is statistically significant AND 
            # the test statistic is smaller than the best test statistic so far.
            if (best_pval < alpha and best_stat > ks_stat):
                best_stat = ks_stat
                best_dist = dist_name
                best_pval = pval

    print(f'Best Distribution Fit: {best_dist}')

    if gen_samples:
        return samples, dist_results
    else:
        return dist_results
