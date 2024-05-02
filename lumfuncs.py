import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class LumFuncTest:
    """
    Parent class for a luminosity function test.
    """
    def __init__(self):
        self.test_type = "Luminosity Function"
        
class StanekWindowLF(LumFuncTest):
    """
    write this

    """
    def __init__(self):
        self.data_source = "Terry et al. 2020"
        self.obs_data = pd.read_csv('data/stanekwindow_lumfuncs.txt', delim_whitespace=True, comment='#', na_values='-')
        self.filters = ['V','I','J','H']
    
    def run_comparison(self, mod_dict, area_mod):
        fig, axs = plt.subplots(2, 2)
        for i,filt in enumerate(self.filters):
            j=int(i/2)
            k=i%2
            axs[j,k].step(self.obs_data[filt], self.obs_data['logN'+filt], where='mid', label='observation')
            axs[j,k].set_ylabel('logN')
            axs[j,k].set_xlabel(filt)

            bin_width=0.3
            mod_bins = np.array(self.obs_data[filt][~np.isnan(self.obs_data[filt])])
            mod_hist = np.log10(np.histogram(mod_dict[filt], bins=mod_bins)[0]/ bin_width / area_mod / 60**2)
            axs[j,k].step((mod_bins[1:]+mod_bins[:-1])/2, mod_hist, where='mid', label='model')
        axs[0,0].legend()
        plt.suptitle("Luminosity functions in Stanek Window\nl,b = 0.25,-2.15, data from Terry et al. 2020")

        fig.tight_layout()
