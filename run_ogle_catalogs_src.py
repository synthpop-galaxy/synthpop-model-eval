from mulens_rates import microlensing_calculations as mulens_rates
import numpy as np
import synthpop as sp
import pandas as pd

ulim = 10000
llim = 3000
alim = 4000

flds = pd.read_csv('subfs_inmap.csv')
mod = sp.SynthPop('huston2025_defaults.synthpop_conf',
                  maglim=["Bessell_I", 21, "remove"],
                  chosen_bands=["Bessell_U", "Bessell_B", "Bessell_V", "Bessell_R", "Bessell_I", 
                                "2MASS_J", "2MASS_H", "2MASS_Ks"],
                  post_processing_kwargs=[{"name":"ProcessDarkCompactObjects", "remove":True}],
                  name_for_output="Huston2025",
                  output_location="outputfiles/ogle_chips/src",
                  skip_lowmass_stars=True,
                  output_file_type="h5"
                 )
mod.init_populations()
solang = 1e-5

for i in flds.index:
    l = flds.GLON[i]
    b = flds.GLAT[i]
    df1,_ = mod.process_location(l_deg=l, b_deg=b, solid_angle=solang)
    leng = len(df1)
    if leng>ulim or leng<llim:
        print('    length:',leng,", rerunning l=",l,' b=',b)
        solang = solang * alim/leng
        df1,_ = mod.process_location(l_deg=l, b_deg=b, solid_angle=solang)
        leng = len(df1)
    solang = solang * alim/leng
