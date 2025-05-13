import synthpop as sp
import numpy as np
import pandas as pd
from astropy.table import Table

def ogle_starcounts():
    # Load needed OGLE data
    ogle_surfdens = Table.read('data/apjsab426b/apjsab426bt5_mrt.txt', format="ascii.cds").to_pandas(index='field')
    subfs_inmap = ogle_surfdens[(np.abs(ogle_surfdens.GLON)<10) & (ogle_surfdens.GLAT<5) & (ogle_surfdens.GLAT>-10)]
    ogle_subf_lbs = subfs_inmap[['GLON','GLAT']].to_numpy()[:3]

    # Set up SynthPop model
    mod = sp.SynthPop(default_config='huston2025_defaults.synthpop_conf',
                              model_name="Huston2025", name_for_output='src_count',
                             maglim=['Bessell_I', 21,"remove"], output_location="outputfiles/ogle",
                              chosen_bands = ['Bessell_I', 'Bessell_V'],
                             post_processing_kwargs = [{"name": "ProcessDarkCompactObjects","remove": True}], 
                             extinction_map_kwargs={"name":"surot"},
                             skip_lowmass_stars=True)
    mod.init_populations()

    # Get stellar densities by subfield
    n21s = np.zeros(len(ogle_subf_lbs))
    n18s = np.zeros(len(ogle_subf_lbs))
    sa_deg = 0.044
    for i, lb in enumerate(ogle_subf_lbs):
        dat, _ = mod.process_location(*lb, solid_angle=sa_deg, solid_angle_unit='deg^2', save_data=False)
        n21s[i] = len(dat)
        n18s[i] = len(dat[dat.Bessell_I<18])

    # Save result
    df = pd.DataFrame({'field':subfs_inmap, 'l':ogle_subf_lbs[:,0], 'b':ogle_subf_lbs[:,1],
                      'n21':n21s, 'n18':n18s, 'sigma21':n21s/sa_deg/3600, 'sigma18':n18s/sa_deg/3600})
    df.to_csv('outputfiles/ogle_sim_surfdens.csv', index=False)
    return df
    
ogle_starcounts()