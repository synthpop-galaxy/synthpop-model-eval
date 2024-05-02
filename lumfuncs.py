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
    def __init__(self):
        self.data_source = "Terry et al. 2020"
        self.obs_data = pd.read_csv('data/stanekwindow_lumfuncs.txt', delim_whitespace=True, comment='#', na_values='-')
        self.filters = ['V','I','J','H']
    
    def run_comparison(self, V_mod, I_mod, J_mod, H_mod, area_mod):
        fig, axs = plt.subplots(2, 2)
        for i,filt in enumerate(self.filters):
            j=int(i/2)
            k=i%2
            axs[j,k].step(self.obs_data[filt], self.obs_data['logN'+filt], where='mid')
            axs[j,k].set_ylabel('logN')
            axs[j,k].set_xlabel(filt)
        fig.tight_layout()
        #axs[0,1].step(self.obs_data['I'], self.obs_data['logNI'], where='mid')
        #axs[1,0].step(self.obs_data['J'], self.obs_data['logNJ'], where='mid')
        #axs[1,1].step(self.obs_data['H'], self.obs_data['logNH'], where='mid')
