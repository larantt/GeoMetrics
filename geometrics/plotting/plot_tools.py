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

import numpy as np                      # for handling arrays
import matplotlib as mpl                # ah... beloved matplotlib
import matplotlib.pyplot as plt         # for creating figures
import cartopy.crs as ccrs              # for creating geospatially referenced figures
import cartopy.feature as cfeature      # interface to cartopy.feature

mpl.style.use('geometrics_stylesheet.mplstyle')

# FOR DEVELOPER REFERENCE - helpful matplotlib stuff
# mpl.colors, mpl.patches, mpl.Line2D, mpl.colors.ListedColormap, mpl.collections.LineCollection, mpl.cm, mpl.colors.Normalize
