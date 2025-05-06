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
from urllib.request import urlretrieve
import os
import gzip
import shutil

ccyc = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', 
        '#984ea3', '#999999', '#e41a1c', '#dede00']

ogle_ews_event_list = ['OGLE-2025-BLG-0467', 'OGLE-2025-BLG-0127', 'OGLE-2025-BLG-0412', 'OGLE-2025-BLG-0110']
ogle_ews_radec_str = [['17:58:53.03', '17:48:50.25', '17:45:37.72', '18:15:26.22'],
                      ['-29:11:29.3', '-37:15:03.9', '-22:35:55.7', '-32:03:54.5']]
ogle_ews_radec_coord = SkyCoord(*ogle_ews_radec_str, unit=(u.hourangle, u.deg))
ogle_ews_lb_coord = ogle_ews_radec_coord.transform_to('galactic')
ogle_ews_lb_flt = np.array([ogle_ews_lb_coord.l.deg, ogle_ews_lb_coord.b.deg])
ogle_ews_solid_angle = 2*2 / (60**2)

# Load files, downloading first if needed
def get_ogle_cutout(event_name, location='data/ogle_ews_cmds/',
                     url_base='https://www.astrouw.edu.pl/ogle/ogle4/ews/'):
    try:
        data = pd.read_csv(location+event_name+'_map.dat', sep='\s+', usecols=[3,5],header=None, names=['V','I'])
    except:
        if not os.path.isdir(location):
            os.mkdir(location)
        name_pts = event_name.split('-')
        ogle_location = name_pts[1]+'/'+name_pts[2].lower()+'-'+name_pts[3]+'/'
        urlretrieve(url_base+ogle_location+'map.dat.gz', location+event_name+'_map.dat.gz')
        urlretrieve(url_base+ogle_location+'params.dat', location+event_name+'_params.dat')
        with gzip.open(location+event_name+'_map.dat.gz', 'rb') as f_in:
            with open(location+event_name+'_map.dat', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        data = pd.read_csv(location+event_name+'_map.dat', sep='\s+', usecols=[3,5],header=None, names=['V','I'])
    return data

def cmds_ogle_ews(model_data, separate_populations=False):
    """
    Module to compare a model catalogs to V,I map data from OGLE EWS.
    Test based on Figure 21 of Lam et al (2020, PopSyCLE paper i)
    input:
        model_data: dictionary with each event from ogle_ews_event_list as a key
            for a sub-dictionary, with each model name as a key for the sub-sub-dictionary
            containing simulated I and V -band photometry
            e.g. {'OGLE-2025-BLG-0467':{'Model1':{'I':[18,13,15], 'V':[15,16,14]}}, ...}
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
    cbins = np.arange(c_min,c_max+0.01,0.25)
    for i,ev in enumerate(events):
        plt.subplot(len(events),cols,1+i*cols)
        if lb_flt[0][i]>180:
            lpnt=360-lb_flt[0][i]
        else:
            lpnt = lb_flt[0][i]
        lstr,bstr = f'{lpnt:3.1f}', f'{lb_flt[1][i]:3.1f}'
        plt.title(ev+' ('+lstr+','+bstr+')')
        dat = get_ogle_cutout(ev)
        dat = dat[(dat['I']<m_min) & (dat['I']>m_max) & (dat['V']-dat['I']>c_min) & (dat['V']-dat['I']<c_max)]
        plt.plot(dat['V']-dat['I'],dat['I'], 'k.')
        plt.text(c_max-1,m_max+0.5,str(len(dat)),c='dimgray')
        plt.xlim(c_min,c_max)
        plt.ylim(m_min,m_max)
        plt.xlabel('V-I')
        plt.ylabel('I')
    
        plt.subplot(len(events),cols,cols-1+i*cols)
        plt.title('Luminosity Function')
        plt.hist(dat['I'],histtype='step',label='OGLE EWS', color='k',bins=mbins)
        plt.xlabel('I')
        plt.subplot(len(events),cols,cols+i*cols)
        plt.title('Color Function')
        plt.hist(dat['V']-dat['I'],histtype='step', color='k',bins=cbins)
        plt.xlabel('V-I')
    
        for j in range(len(models)):
            all_dat = model_data[ev][models[j]]
            cdat = all_dat[(all_dat['I']<m_min) & (all_dat['I']>m_max) & (all_dat['V']-all_dat['I']>c_min) & (all_dat['V']-all_dat['I']<c_max)]
            plt.subplot(len(events),cols,2+j+i*cols)
            plt.title(models[j])
            if not separate_populations:
                plt.plot(cdat['V']-cdat['I'],cdat['I'], 'k.')
            else:
                pp = cdat['pop']==0.0
                plt.plot(cdat['V'][pp]-cdat['I'][pp],cdat['I'][pp], marker='.',linestyle='none',c=ccyc[0], label='bulge')
                pp = (cdat['pop']>0.0) & (cdat['pop']<3.0)
                plt.plot(cdat['V'][pp]-cdat['I'][pp],cdat['I'][pp], marker='.',linestyle='none',c='gray')
                pp = cdat['pop']>3.0
                plt.plot(cdat['V'][pp]-cdat['I'][pp],cdat['I'][pp], marker='.',linestyle='none',c=ccyc[1], label='disk')
                plt.legend(loc=2)
            plt.text(c_max-1,m_max+0.5,str(len(cdat)),c='dimgray')
            plt.xlim(c_min,c_max)
            plt.ylim(m_min,m_max)
            plt.xlabel('V-I')
            plt.ylabel('I')
    
            plt.subplot(len(events),cols,cols-1+i*cols)
            plt.hist(cdat['I'], histtype='step',label=models[j],bins=mbins,linestyle='--')
            plt.subplot(len(events),cols,cols+i*cols)
            plt.hist(cdat['V']-cdat['I'], histtype='step',bins=cbins,linestyle='--')

    
        plt.subplot(len(events),cols,cols-1+i*cols)
        plt.legend()
    
        plt.tight_layout()
