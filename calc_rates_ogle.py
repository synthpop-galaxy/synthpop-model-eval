import numpy as np
from mulens_rates import microlensing_calculations
import pandas as pd
import time
import pdb

chips = pd.read_csv('subfs_inmap.csv')

data_list = []
for i in chips.index:
    l = chips.GLON[i]
    b = chips.GLAT[i]
    f_lens = f'outputfiles/ogle_chips/lens/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
    f_src = f'outputfiles/ogle_chips/src/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
    try:
        dat,output_cols = microlensing_calculations.mulens_stats(l, b, f_lens, f_src, 
            nsd=True, field_id=i, tE_range=[0,300])
        data_list.append(dat)
        print(i, *dat[:4])
    except:
        data_list.append([l,b]+list(np.repeat(np.nan,len(dat)-2)))
        print(i, l, b, 'NO MATCHES')
output = pd.DataFrame(data=data_list, columns=output_cols)
output.to_csv('mulens_rates_ogle_0tE300.txt', index=False)

