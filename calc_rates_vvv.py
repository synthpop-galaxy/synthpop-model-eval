import numpy as np
from mulens_rates import microlensing_calculations
import pandas as pd
import time
import pdb

data_list = []
i=0

for b in np.arange(-10.0, 5.0, 0.25)+0.125:
    for l in np.arange(-4.0, 4.0, 0.25)+0.125:
        f_lens = f'outputfiles/vvv_kacz/lens/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        f_src = f'outputfiles/vvv_kacz/src18/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        dat,output_cols = microlensing_calculations.mulens_stats_alt(l, b, f_lens, f_src,nsd=False,cut_nsd=False, field_id=i,
                                    tE_range=[3,300], mag_band='VISTA_Ks', mag_cut=17)
        data_list.append(dat)
        print(i, *dat[:4])
        i+=1
output = pd.DataFrame(data=data_list, columns=output_cols)
output.to_csv('mulens_rates_vvv_3tE300_mag17.txt', index=False)

data_list = []
i=0
for b in np.arange(-2.5, 2.5, 0.25)+0.125:
    for l in np.arange(-4.0, 4.0, 0.25)+0.125:
        f_lens = f'outputfiles/vvv_kacz/lens/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        f_src = f'outputfiles/vvv_kacz/src18/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        dat,output_cols = microlensing_calculations.mulens_stats_alt(l, b, f_lens, f_src,nsd=False,cut_nsd=True, field_id=i,
                                    tE_range=[3,300], mag_band='VISTA_Ks', mag_cut=17)
        data_list.append(dat)
        print(i, *dat[:4])
        i+=1
output = pd.DataFrame(data=data_list, columns=output_cols)
output.to_csv('mulens_rates_vvv_nonsd_3tE300_mag17.txt', index=False)

data_list = []
i=0
for b in np.arange(-2.5, 2.5, 0.25)+0.125:
    for l in np.arange(-4.0, 4.0, 0.25)+0.125:
        f_lens = f'outputfiles/vvv_kacz/lens/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        f_src = f'outputfiles/vvv_kacz/src18/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        dat,output_cols = microlensing_calculations.mulens_stats_alt(l, b, f_lens, f_src,nsd=False,cut_nsd=True, field_id=i,
                                    tE_range=[3,300], mag_band='VISTA_Ks', mag_cut=17)
        data_list.append(dat)
        print(i, *dat[:4])
        i+=1
output = pd.DataFrame(data=data_list, columns=output_cols)
output.to_csv('mulens_rates_vvv_nonsd_3tE300_mag18.txt', index=False)