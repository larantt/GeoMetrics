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
from matplotlib.lines import Line2D     # for spoofing legends

#mpl.style.use('geometrics_stylesheet.mplstyle')

#############
## GLOBALS ##
#############

# Tol color pallete
lgrey = "#d3d3d3"
indigo = "#332288"
grass = "#117733"
teal = "#44AA99"
sky = "#88CCEE"
mustard = "#DDCC77"
blush = "#CC6677"
fuscia = "#AA4499"
mauve = "#882255"

# IBM color pallete
ibm_blue = "#648FFF"
ibm_purple = "#785EF0"
ibm_pink = "#DC267F"
ibm_oragne = "#FE6100"
ibm_yellow = "#FFB000"

# Nice printing in the terminal
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'

# FOR DEVELOPER REFERENCE - helpful matplotlib stuff
# mpl.colors, mpl.patches, mpl.Line2D, mpl.colors.ListedColormap, mpl.collections.LineCollection, mpl.cm, mpl.colors.Normalize

def plot_histogram(data,bins='sqrt',comp_distribution=None,ax=None,labels=None,ks_alpha=0.05):
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

    ks_alpha : float
        significance level to use for the Kolmogorov-Smirnov test
        if a comparative distribution is supplied

    Returns
    -------
    """
    # set labels to empty list if unspecified
    if not labels:
        labels = []
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
    #print(nbins)

    if comp_distribution:
        # take samples from the equivalent theoretical distribution
        theor_dist, _ = sc.get_theoretical_dist(distributions[0],comp_distribution)

        # test the fit of the distribution using kolmogorov smirnov
        for dist_obs, lab in zip(distributions,labels):
            ks_stat, pval = scipy.stats.ks_2samp(dist_obs, theor_dist)

            # formatting for p-value
            if pval < 0.0001:
                print_pval = '< 0.0001'
            elif round(pval,3) == 0:
                print_pval = round(pval,4)
            else:
                print_pval = round(pval,3)
            
            # print conclusion of ks test
            if pval > ks_alpha:
                print(f'Kolmogorov-Smirnov Test finds distribution to be {GREEN}statistically similar{END} to a {comp_distribution} distribution at a {ks_alpha} signifcance level')
            else:
                print(f'Kolmogorov-Smirnov Test finds distribution to be {RED}statistically different{END} to a {comp_distribution} distribution at a {ks_alpha} signifcance level')
            
            # get maximum of both distributions
            ypos = max(*distributions)
            xpos = nbins
            ax.text(xpos,ypos,f'K-S Test Statistic: {round(ks_stat,3)}\nP-Value: {print_pval}')
        
        # append to the correct lists
        distributions.append(theor_dist)
        labels.append(comp_distribution)

        # set title
        ax.set_title(f'Histogram of Input Data with {comp_distribution} Overlay',loc='left') # REMINDER: ADD AUTOCAPS TO DIST
    else:
        ax.set_title('Histogram of Input Data',loc='left')

    # format axes
    ax.hist(distributions,int(nbins),label=labels)
    ax.legend()
    ax.set_title(f'{int(nbins)} Bins',loc='right')



def generate_table(desired_stats,thresholds=None):
    """
    Function generates a nicely formatted table which 
    summarises statistics contained in a dictionary. This 
    can be categoriesed by "goodness" thresholds taken from
    Prof. Liemohn's textbook if on.

    Parameters
    ----------
    desired_stats : dict
        Dictionary containing variable names and statistics
        Should be ordered with the key as the label in the table
        and the value as the variable.
    thresholds : dict
        Dictionary containing thresholds for statistics provided in
        desired_stats. Note that the keys in each dictionary must match
        or the function will fail.

    Returns
    -------
    """
    # determine the number of rows and columns in the table
    rows = len(desired_stats) # get the length of the desired list of statistics
    cols = len(desired_stats[0].keys())    # return the number of keys, should be the same for all entries

    # create figure
    fig, ax = plt.subplots(figsize=(rows*1.5,cols*1.8))

    # set up the axis limits with "spacing" (a bit of padding on each side)
    ax.set_ylim(-1, rows + 1)
    ax.set_xlim(0, cols + .1)

    # format the table
    for row in range(rows):
        ax.plot(
            [0, cols + 1],
            [row -.5, row - .5],
            ls=':',
            lw='.5',
            c='grey'
        )
    
    # add header row differentiator
    ax.plot([0, cols + 1], [rows-.5, rows-.5], lw='1', c='black')
    ax.plot([0, cols + 1], [rows+.5, rows+.5], lw='1', c='black')

    # hide axes
    ax.axis('off')

    # add nice differentiator shading for the row labels
    rect = mpl.patches.Rectangle(
        (0, -.5),  # bottom left starting position (x,y)
        .95 * 1.5,  # width
        rows,  # height
        ec='none',
        fc='grey',
        alpha=.2,
        zorder=-1
    )
    ax.add_patch(rect)

    # loop over data to populate table in reverse order (x=0 is at the bottom)
    for row,metric in enumerate(reversed(desired_stats)):
        
        # loop over columns to add to figure
        for pos,key in enumerate(metric.keys()):
            # check if is label for column
            if key == 'metric':
                ax.text(x=.1, y=row, s=metric[key],va='center', ha='left', weight='bold')
            # check if threshold    
            elif key == 'threshold':
                ax.text(x=pos+.5, y=row, s=metric[key],va='center', ha='left', weight='bold')
                # add dotted line after threshold
                ax.plot([pos+1.32,pos+1.32], [-0.5,rows-.5], ls=':', lw=.5, c='lightgrey',zorder=1)

            if thresholds != None:
                # remember, order of variables is (score, success rate)
                #check for NaNs
                if np.isnan(metric[key][0]):
                    color = 'k'
                # check if the value is good, bad or okay
                elif metric[key][1] == 'good':
                    color = grass

                elif metric[key][1] == 'bad':
                    color = mauve

                else:
                    color = 'k'
                    
                # now plot in the correct color
                ax.text(x=pos+.5, y=row, s=round(metric[key][0],2),va='center', ha='left', weight='bold',c=color)

    # add title to table
    #ax.set_title(f"Event Detection Metrics Summary Table {subset_method}",fontsize=16,fontweight='bold')

    # spoof a legend below the title to explain the color codes
    custom_lines = [Line2D([0], [0], color=grass, lw=4),
                    Line2D([0], [0], color=mauve, lw=4),
                    Line2D([0], [0], color='k', lw=4)]
    
    ax.legend(custom_lines, 
              ['Good Performance', 'Poor Performance'], 
              ncol=2,
              loc='center', bbox_to_anchor=(0.5,0.986),
              frameon=False)