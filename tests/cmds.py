"""
Module containing methods to test models against 
observed color-magnitude diagrams
Current options are:
    cmds_ogle_ews(model_data)
"""

import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
import matplotlib.pyplot as plt
import pandas as pd

ogle_ews_event_list = ['ob240223','og240001', 'ob240475','ob240521']
ogle_ews_radec_str = [['17:53:53.93','16:47:10.74','17:23:12.85','18:04:24.43'],
             ['-28:37:10.5','-39:53:57.0','-29:45:42.9','-27:33:58.2']]
ogle_ews_radec_coord = SkyCoord(*ogle_ews_radec_str, unit=(u.hourangle, u.deg))
ogle_ews_lb_coord = ogle_ews_radec_coord.transform_to('galactic')
ogle_ews_lb_flt = np.array([ogle_ews_lb_coord.l.deg, ogle_ews_lb_coord.b.deg])
ogle_ews_solid_angle = 2*2 / (60**2)

def cmds_ogle_ews(model_data):
    """
    Module to compare a model catalogs to V,I map data from OGLE EWS.
    Test based on Figure 21 of Lam et al (2020, PopSyCLE paper i)
    input:
        model_data: dictionary with each event from ogle_ews_event_list as a key
            for a sub-dictionary, with each model name as a key for the sub-sub-dictionary
            containing simulated I and V -band photometry
            e.g. {'ob240223':{'Model1':{'I':[18,13,15], 'V':[15,16,14]}}, ...}
    output:
        a grid of CMD plots for OGLE EWS data and each model, and luminosity and color functions
    """
    events = ogle_ews_event_list
    lb_flt = ogle_ews_lb_flt
    cols = 3+len(model_data[events[0]])
    models = list(model_data[events[0]].keys())
    plt.subplots(nrows=len(events),ncols=cols, figsize=(4*cols,4*len(events)))
    m_min, m_max = 18,12
    c_min, c_max = 0,5
    mbins = np.arange(m_max,m_min+0.01,0.5)
    cbins = np.arange(c_min,c_max+0.01,0.5)
    for i,ev in enumerate(events):
        plt.subplot(len(events),cols,1+i*cols)
        if lb_flt[0][i]>180:
            lpnt=360-lb_flt[0][i]
        else:
            lpnt = lb_flt[0][i]
        lstr,bstr = f'{lpnt:3.1f}', f'{lb_flt[1][i]:3.1f}'
        plt.title(ev+' ('+lstr+','+bstr+')')
        dat = pd.read_csv('data/'+ev+'_map.dat',sep='\s+', usecols=[3,5],comment='#')
        dat = dat[(dat['I']<m_min) & (dat['I']>m_max) & (dat['V']-dat['I']>c_min) & (dat['V']-dat['I']<c_max)]
        plt.plot(dat['V']-dat['I'],dat['I'], 'k.')
        plt.text(c_max-1,m_max+0.5,str(len(dat)),c='b')
        plt.xlim(c_min,c_max)
        plt.ylim(m_min,m_max)
    
        plt.subplot(len(events),cols,cols-1+i*cols)
        plt.title('Luminosity Function')
        plt.hist(dat['I'],histtype='step',label='OGLE EWS', color='k',bins=mbins)
        plt.subplot(len(events),cols,cols+i*cols)
        plt.title('Color Function')
        plt.hist(dat['V']-dat['I'],histtype='step', color='k',bins=cbins)
    
        for j in range(len(models)):
            all_dat = model_data[ev][models[j]]
            cdat = all_dat[(all_dat['I']<m_min) & (all_dat['I']>m_max) & (all_dat['V']-all_dat['I']>c_min) & (all_dat['V']-all_dat['I']<c_max)]
            plt.subplot(len(events),cols,2+j+i*cols)
            plt.title(models[j])
            plt.plot(cdat['V']-cdat['I'],cdat['I'], 'k.')
            plt.text(c_max-1,m_max+0.5,str(len(cdat)),c='b')
            plt.xlim(c_min,c_max)
            plt.ylim(m_min,m_max)
    
            plt.subplot(len(events),cols,cols-1+i*cols)
            plt.hist(cdat['I'], histtype='step',label=models[j],bins=mbins,linestyle='--')
            plt.subplot(len(events),cols,cols+i*cols)
            plt.hist(cdat['V']-cdat['I'], histtype='step',bins=cbins,linestyle='--')
    
        plt.subplot(len(events),cols,cols-1+i*cols)
        plt.legend()
    
        plt.tight_layout()
