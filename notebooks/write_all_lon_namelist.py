"""
Write a long data.ecco file for all of those longitudes
"""

import os
import numpy as np

def get_header():
    return "#\n"+ \
            "# ******************\n"+ \
            "# ECCO cost function\n"+ \
            "# ******************\n"+ \
            "#\n" + \
            " &ECCO_COST_NML\n" + \
            " cost_iprec  = 32,\n" + \
            " cost_yftype = 'RL',\n" + \
            " /\n" + \
            "#\n" + \
            " &ECCO_GENCOST_NML\n"+ \
            "#\n"


def get_single_gencost(lon_str, klev, kgen):
    return  f" gencost_name({kgen})        = 'uvel_{lon_str}_{klev:02}k',\n" + \
            f" gencost_avgperiod({kgen})   = 'const',\n" + \
            f" gencost_barfile({kgen})     = 'm_horflux_vol',\n" + \
            f" gencost_mask({kgen})        = 'masks_all_lon/uvel_{lon_str}_{klev:02}k_'\n" + \
            f" gencost_outputlevel({kgen}) = 0,\n" + \
            f" mult_gencost({kgen})        = 1,\n"

def get_single_lon(lon_str,kgen_start):
    mylon =f"# --- {lon_str}\n" + \
            "#\n"

    for k in range(22):
        mylon+=get_single_gencost(lon_str,k,kgen=kgen_start+k)
        mylon+="#\n"

    return mylon

if __name__ == "__main__":
    eccostr = get_header()
    all_lons = ['110W','140W','170W','165E','156E','147E']
    lon_kgen = np.arange(1,133,22)
    for lon,kgen in zip(all_lons,lon_kgen):
        eccostr+=get_single_lon(lon,kgen)

    eccostr+=" /\n"

    # write it out
    write_dir = 'masks_all_lon'
    if not os.path.isdir(write_dir):
        os.makedirs(write_dir)

    namelistpath = f'{write_dir}/data.ecco'
    with open(namelistpath,'w') as f:
        f.write(eccostr)
