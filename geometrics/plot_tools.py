#usr/bin/env/ python
"""
plot_tools.py

Author: Lara Tobias-Tarsh (laratt@umich.edu)
Created: 21/06/2024

This is a module intended to obfuscate the long, painful lines of formatting 
code needed in matplotlib to create attractive plots, especially when 
integrated with cartopy for geospatial analysis.
"""

#---------#
# IMPORTS #
#---------#
import datetime as dt
import geometrics.stats_calcs as sc

import numpy as np                      # for handling arrays
import matplotlib as mpl                # ah... beloved matplotlib
import matplotlib.pyplot as plt         # for creating figures
import cartopy.crs as ccrs              # for creating geospatially referenced figures
import cartopy.feature as cfeature      # interface to cartopy.feature
import scipy

#mpl.style.use('geometrics_stylesheet.mplstyle')

# FOR DEVELOPER REFERENCE - helpful matplotlib stuff
# mpl.colors, mpl.patches, mpl.Line2D, mpl.colors.ListedColormap, mpl.collections.LineCollection, mpl.cm, mpl.colors.Normalize

def plot_histogram(data,bins='sqrt',comp_distribution=None,ax=None,labels=[]):
    """
    Function to generate a nice histogram of n sets of 
    data. Can be used to compare multiple datasets or to
    compare data to an equivalent distribution (e.g. normal)

    Parameters
    ----------
    data : Any
        Input data to function. Valid types are
        arrays or dictionaries containing labelled arrays
    
    nbins : string or int
        Number of bins to show in histogram or kwarg that
        can be used to define number of bins in histogram

    comp_distribution : string, ArrayLike, dict
        Distribution to compare input data to if desired.
        Can be passed as a string to be defined internally, a
        dictionary of multiple comparison distributions or an 
        array of a predefined distribution.
    
    ax : mpl.Axes
        matplotlib axes on which to plot histogram

    labels : list
        list of string labels to use in histogram plot

    Returns
    -------
    """
    # check if axes are defined in function already (maybe move this later to save time)
    if not ax:
        # if axis not defined, create a figure and axis for plot
        fig, ax = plt.subplots(1,1)
    
    # check data type
    if isinstance(data,np.ndarray):
        distributions = [data]  # wrap data in list for continuity in function
    elif isinstance(data,dict):
        # extract the individual datasets and their labels
        labels,distributions = list(data.keys()),list(data.values())
    else:
        raise(TypeError(f'invalid datatype {type(data)}. Ensure type is an array or dictionary of arrays'))
    
    # define number of bins (assumes this is of the LARGEST dataset)
    nbins = sc.histogram_bins(len(max(distributions, key=len)),bins)
    print(nbins)

    if comp_distribution:
        # take samples from the equivalent theoretical distribution
        theor_dist, _ = sc.get_theoretical_dist(distributions[0],comp_distribution)

        # test the fit of the distribution using kolmogorov smirnov
        for dist_obs, lab in zip(distributions,labels):
            ks_stat, pval, _, _ = scipy.stats.ks_2samp(dist_obs, theor_dist)
            # ADD WHEN FORMATTING COMPLETED: annotate on graph
        
        # append to the correct lists
        distributions.append(theor_dist)
        labels.append(comp_distribution)

    ax.hist(distributions,int(nbins),label=labels)
    ax.legend()
    



