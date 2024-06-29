#usr/bin/env/ python
"""
utils.py

Author: Lara Tobias-Tarsh (laratt@umich.edu)
Created: 28/06/2024

Utility module for random extra functions used to
supplement the GeoMetrics package.
"""

import numpy as np

def csv_to_dict(path,missing='M'):
    """
    Function uses genfromtxt to read a csv to
    a dictionary nicely. 
    
    Currently very lazy basic function that could be
    expanded into an actually good file reader later.

    Parameters
    ----------
    path : str
        path to csv file
    missing : Any
        missing value in csv data. Refer to np.genfromtxt for kwargs.
    """
    data = np.genfromtxt(path, delimiter=',', names=True, dtype=None, encoding=None, autostrip=True,missing_values=missing)
    data_dict = {col: data[col] for col in data.dtype.names}
    return data_dict