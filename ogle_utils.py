"""
A bunch of useful python scripts that:
* return equatorial/Galactic coordinates of vertices of OGLE-IV fields
* plot OGLE-IV fields/subfields in equatorial/Galactic coordinates

P. Mroz, 26 May 2019
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

PIXEL_SIZE = 0.2585 # 1 pix = 0.2585 arcsec

def o4_field (ra0, dec0):
    """ 
    Returns the equatorial coordinates of vertices of an OGLE-IV field
    centered on (ra0, dec0).
    """
    ra, dec = [], []
    pix = PIXEL_SIZE / 3600.0
    pixra = PIXEL_SIZE / 3600.0 / np.cos(dec0*np.pi/180.0)
    ra.append(ra0-7518.0*pixra)
    dec.append(dec0+4321.0*pix)
    ra.append(ra0-7518.0*pixra)
    dec.append(dec0+8610.0*pix)
    ra.append(ra0+7518.0*pixra)
    dec.append(dec0+8610.0*pix)
    ra.append(ra0+7518.0*pixra)
    dec.append(dec0+4321.0*pix)
    ra.append(ra0+9616.0*pixra)
    dec.append(dec0+4321.0*pix)
    ra.append(ra0+9616.0*pixra)
    dec.append(dec0-4321.0*pix)
    ra.append(ra0+7518.0*pixra)
    dec.append(dec0-4321.0*pix)
    ra.append(ra0+7518.0*pixra)
    dec.append(dec0-8610.0*pix)
    ra.append(ra0-7518.0*pixra)
    dec.append(dec0-8610.0*pix)
    ra.append(ra0-7518.0*pixra)
    dec.append(dec0-4321.0*pix)
    ra.append(ra0-9616.0*pixra)
    dec.append(dec0-4321.0*pix)
    ra.append(ra0-9616.0*pixra)
    dec.append(dec0+4321.0*pix)
    
    return np.array(ra), np.array(dec)
    
def o4_subfield (ra0, dec0, chip):
    """ 
    Returns the equatorial coordinates of vertices of an OGLE-IV subfield
    centered on (ra0, dec0).
    """
    ra, dec = [], []
    pix = PIXEL_SIZE / 3600.0
    pixra = PIXEL_SIZE / 3600.0 / np.cos(dec0*np.pi/180.0)
    
    assert type(chip) is int, 'chip is not an integer: %r' % chip
    assert chip >=1 and chip <= 32, 'chip >=1 and chip <= 32'
    
    if chip >= 1 and chip <= 7:
        ra.append(ra0+7468.0*pixra-(chip-1.0)*2148.0*pixra)
        dec.append(dec0-8610.0*pix)
        ra.append(ra0+7468.0*pixra-(chip-1.0)*2148.0*pixra)
        dec.append(dec0-4508.0*pix)
        ra.append(ra0+5420.0*pixra-(chip-1.0)*2148.0*pixra)
        dec.append(dec0-4508.0*pix)
        ra.append(ra0+5420.0*pixra-(chip-1.0)*2148.0*pixra)
        dec.append(dec0-8610.0*pix)
    elif chip >= 8 and chip <= 16:
        ra.append(ra0+9616.0*pixra-(chip-8.0)*2148.0*pixra)
        dec.append(dec0-4134.0*pix)
        ra.append(ra0+9616.0*pixra-(chip-8.0)*2148.0*pixra)
        dec.append(dec0-32.0*pix)
        ra.append(ra0+7568.0*pixra-(chip-8.0)*2148.0*pixra)
        dec.append(dec0-32.0*pix)
        ra.append(ra0+7568.0*pixra-(chip-8.0)*2148.0*pixra)
        dec.append(dec0-4134.0*pix)
    elif chip >= 17 and chip <= 25:
        ra.append(ra0+9616.0*pixra-(chip-17.0)*2148.0*pixra)
        dec.append(dec0+4134.0*pix)
        ra.append(ra0+9616.0*pixra-(chip-17.0)*2148.0*pixra)
        dec.append(dec0+32.0*pix)
        ra.append(ra0+7568.0*pixra-(chip-17.0)*2148.0*pixra)
        dec.append(dec0+32.0*pix)
        ra.append(ra0+7568.0*pixra-(chip-17.0)*2148.0*pixra)
        dec.append(dec0+4134.0*pix)
    elif chip >= 26 and chip <= 32:
        ra.append(ra0+7468.0*pixra-(chip-26.0)*2148.0*pixra)
        dec.append(dec0+8610.0*pix)
        ra.append(ra0+7468.0*pixra-(chip-26.0)*2148.0*pixra)
        dec.append(dec0+4508.0*pix)
        ra.append(ra0+5420.0*pixra-(chip-26.0)*2148.0*pixra)
        dec.append(dec0+4508.0*pix)
        ra.append(ra0+5420.0*pixra-(chip-26.0)*2148.0*pixra)
        dec.append(dec0+8610.0*pix)

    return np.array(ra), np.array(dec)

def equatorial_to_galactic (_ra, _dec):
    """ Transforming equatorial to Galactic coordinates"""
    deg = np.pi/180.0
    ra_g = 192.85948*deg
    dec_g = 27.12825*deg
    l_NGP = 122.93192*deg
    ra = _ra*deg
    dec = _dec*deg
    sinb = np.cos(dec)*np.cos(dec_g)*np.cos(ra-ra_g)+np.sin(dec)*np.sin(dec_g)
    sinlcosb = np.cos(dec)*np.sin(ra-ra_g)
    coslcosb = np.sin(dec)*np.cos(dec_g)-np.cos(dec)*np.sin(dec_g)*np.cos(ra-ra_g)
    b = np.arcsin(sinb)
    l = np.arctan2(sinlcosb,coslcosb)
    l = l_NGP - l
    b /= deg
    l /= deg
    l[l>180] -= 360.0
    return l, b