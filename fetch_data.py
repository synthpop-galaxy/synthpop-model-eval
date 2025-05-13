import os
from astropy.table import Table
from urllib.request import urlretrieve
import pandas as pd
import gzip
import shutil

# Load machine readable table from AAS journals, downloading first if needed
def get_aasjournals_table(file_name, location, url_base):
    try:
        data = Table.read(location+file_name, format="ascii.cds")
    except:
        if not os.path.isdir(location):
            os.mkdir(location)
        urlretrieve(url_base+file_name, location+file_name)
        data = Table.read(location+file_name, format="ascii.cds")
    return data

def ogle_mroz2019(location='data/apjsab426b/',
                     url_base='https://content.cld.iop.org/journals/0067-0049/244/2/29/revision1/'):
    tab_surf_dens = get_aasjournals_table('apjsab426bt5_mrt.txt', location, url_base).to_pandas(index='field')
    tab_fields = get_aasjournals_table('apjsab426bt6_mrt.txt', location, url_base).to_pandas(index='field')
    tab_rates = get_aasjournals_table('apjsab426bt7_mrt.txt', location, url_base).to_pandas(index='field')
    return tab_surf_dens, tab_fields, tab_rates

def ogle_ews_mapdat(event_list=['OGLE-2025-BLG-0467', 'OGLE-2025-BLG-0127', 'OGLE-2025-BLG-0412', 'OGLE-2025-BLG-0110'], 
                      location='data/ogle_ews_cmds/',
                      url_base='https://www.astrouw.edu.pl/ogle/ogle4/ews/'):
    data_dict = {}
    for event_name in event_list:
        try:
            data_dict[event_name] = pd.read_csv(location+event_name+'_map.dat', sep='\s+', usecols=[3,5],header=None, names=['V','I'])
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
            data_dict[event_name] = pd.read_csv(location+event_name+'_map.dat', sep='\s+', usecols=[3,5],header=None, names=['V','I'])
    return data_dict