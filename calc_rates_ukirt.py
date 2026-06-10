import numpy as np
from mulens_rates import microlensing_calculations
import pandas as pd
import time
import pdb


data_list = []
i=0
for b in np.arange(-2, 0.5, 0.1)+0.05:
    for l in np.arange(-1.0, 1.0, 0.1)+0.05:
        f_lens = f'outputfiles/ukirt/lens/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        f_src = f'outputfiles/ukirt/src_k/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        dat,output_cols = microlensing_calculations.mulens_stats_alt(l, b, f_lens, f_src, nsd=True, field_id=i,
                                    tE_range=[1.5,350])
        data_list.append(dat)
        print(i, *dat[:4])
        i+=1
output = pd.DataFrame(data=data_list, columns=output_cols)
output.to_csv('mulens_rates_ukirt_k_1.5tE350.txt', index=False)


data_list = []
i=0
for b in np.arange(-2, 0.5, 0.1)+0.05:
    for l in np.arange(-1.0, 1.0, 0.1)+0.05:
        f_lens = f'outputfiles/ukirt/lens/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        f_src = f'outputfiles/ukirt/src_h/Huston2025_l{l:2.3f}_b{b:2.3f}.h5'
        dat,output_cols = microlensing_calculations.mulens_stats_alt(l, b, f_lens, f_src, nsd=True, field_id=i,
                                    tE_range=[1.5,350])
        data_list.append(dat)
        print(i, *dat[:4])
        i+=1
output = pd.DataFrame(data=data_list, columns=output_cols)
output.to_csv('mulens_rates_ukirt_h_1.5tE350.txt', index=False)
