"""
Module containing methods to test models against 
observed luminosity functions.
Current options are:
    compare_stanekwindow(model_data, model_area)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
    
def compare_stanekwindow(model_datasets, model_area, model_names):
    """
    Module to compare a model catalog to the luminosity functions in the Stanek Window
    (l,b = 0.25,-2.15) from Terry et al. 2020.
    inputs:
        model_datasets: array containing dictionaries containing the following data arrays for the model catalog:
            {'V', 'I', 'J', 'H'} (apparent magnitudes)
        model_area: array of the areas the size of the catalog region in degrees^2 of each model (in order of inputted into model_datasets)
        model_names: array containing strings of the name of each model (in order of inputted into model_datasets)
    output:
        a plot of the luminosity function histograms for each band
    """
    obs_data = pd.read_csv('data/stanekwindow_lumfuncs.txt', delim_whitespace=True, comment='#', na_values='-')
    filters = ['V','I','J','H']
    fig, axs = plt.subplots(2, 2)
    for i,filt in enumerate(filters):
        j=int(i/2)
        k=i%2
        axs[j,k].step(obs_data[filt], obs_data['logN'+filt], where='mid', label='observation')
        axs[j,k].set_ylabel('logN')
        axs[j,k].set_xlabel(filt)

        bin_width=0.3
        mod_bins = np.array(obs_data[filt][~np.isnan(obs_data[filt])])
        
        index = 0
        
        for model in model_datasets:
            mod_hist = np.log10(np.histogram(model[filt], bins=mod_bins)[0]/ bin_width / model_area[index] / 60**2)
            axs[j,k].step((mod_bins[1:]+mod_bins[:-1])/2, mod_hist, where='mid', label = model_names[index])
            index += 1
            
    axs[0,0].legend()
    plt.suptitle("Luminosity functions in Stanek Window\nl,b = 0.25,-2.15, data from Terry et al. 2020")
    fig.tight_layout()
