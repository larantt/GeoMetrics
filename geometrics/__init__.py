#GeoMetrics/__init__.py

"""
__init__.py defines imports and initialisation for 
the GeoMetrics package.
"""

# import other necessary libraries for initialisation
import os
import matplotlib.pyplot as plt

# import plotting functions here
from .plot_tools import *
from .stats_calcs import *
from .geometrics import *

# Get the path of the current file (i.e., __init__.py)
current_file_path = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the style sheet file
style_path = os.path.join(current_file_path, 'geometrics_stylesheet.mplstyle')

# Load the style sheet
plt.style.use(style_path)
