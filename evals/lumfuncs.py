"""
Module containing methods to test models against 
observed luminosity functions.
Current options are:
    compare_stanekwindow(model_data, model_area)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlretrieve
import os
import gzip
import shutil

def get_terry2020_lf(location='data/apjab629b/'):
    data_url = 'https://iopscience.iop.org/0004-637X/889/2/126/suppdata/apjab629bt5_ascii.txt?doi=10.3847/1538-4357/ab629b'
    file_name = 'apjab629bt5_ascii.txt'
    try:
        data = pd.read_csv(location+file_name, sep='\s+', skiprows=5, skipfooter=1, header=None, engine='python',
                          names=['V', 'logN_V', 'I', 'logN_I', 'J', 'logN_J', 'H', 'logN_H'])
    except:
        if not os.path.isdir(location):
            os.mkdir(location)
        urlretrieve(data_url, location+file_name)
        data = pd.read_csv(location+file_name, sep='\s+', skiprows=5, skipfooter=1, header=None, engine='python', 
                          names=['V', 'logN_V', 'I', 'logN_I', 'J', 'logN_J', 'H', 'logN_H'])
    return data
    
def compare_stanekwindow(model_data, model_area, model_filt_cors=None, obs_filt_cors=None,
                            use_filters=['V','I','J','H']):
    """
    Module to compare a model catalog to the luminosity functions in the Stanek Window
    (l,b = 0.25,-2.15) from Terry et al. 2020.
    inputs:
        model_data: dictionary containing the following data arrays for the model catalog:
            {'V', 'I', 'J', 'H'} (apparent magnitudes)
        model_area: the size of the catalog region in degrees^2
    output:
        a plot of the luminosity function histograms for each band
    """
    obs_data = get_terry2020_lf()
    filt_list = {'V':'WFC3_UVIS_F555W','I':'WFC3_UVIS_F814W','J':'WFC3_IR_F110W','H':'WFC3_IR_F160W'}
    fig, axs = plt.subplots(1,len(use_filters),figsize=(3.5*len(use_filters),4))
    for i,filt in enumerate(use_filters):
        if obs_filt_cors is not None:
            obs_data[filt] = obs_data[filt] + obs_filt_cors[i]
        axs[i].step(obs_data[filt], obs_data['logN_'+filt], where='mid', label='observation')
        axs[i].set_ylabel('logN', fontsize=14)
        axs[i].set_xlabel(filt,fontsize=14)

        bin_width=0.3
        mod_bins = np.array(obs_data[filt][~np.isnan(obs_data[filt])])
        mod_filt = filt_list[filt]
        if model_filt_cors is not None:
            model_data[mod_filt] = model_data[mod_filt]-model_filt_cors[i]
        mod_hist = np.log10(np.histogram(model_data[mod_filt], bins=mod_bins)[0]/ bin_width / model_area / 60**2)
        axs[i].step((mod_bins[1:]+mod_bins[:-1])/2, mod_hist, where='mid', label='model')
    axs[0].legend()
    plt.suptitle("Luminosity functions toward the Stanek Window\n(l,b) = (0.25,-2.15), data from Terry et al. (2020)")
    fig.tight_layout()
    return fig