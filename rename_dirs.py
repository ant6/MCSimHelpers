"""
This script iterates over generated run_* dirs and extracts info about plexi thickness
in a hardcoded place (in geo.dat file). It then renames run_* directories to [thickness]mm
"""

import os

for mc_result_dir in os.listdir('.'):
    curr_thickness = None
    if "run_" in mc_result_dir:
        print("Contents of: ", mc_result_dir)
        os.chdir(os.path.join(mc_result_dir, 'input'))
        with open('geo.dat', 'r') as geo_f:
            tmp_geo = geo_f.readlines()
            curr_thickness = tmp_geo[6].strip('\n').strip('\r')[-8:]
            print(curr_thickness)
        
        os.chdir(os.path.join('..', '..'))
        if curr_thickness:
            os.rename(mc_result_dir, str(curr_thickness) + 'mm')
        else:
            raise ValueError()
