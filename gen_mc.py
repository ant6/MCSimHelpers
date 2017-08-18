"""
WIP

This script generates MC simulation projects with input data ready to start.
It uses mcpartools and assumes user has installed all other dependencies like MC tool itself.
"""

import time
import sys
from shutil import move
from os import fdopen, remove
from os.path import join
from tempfile import mkstemp

from mcpartools.generatemc import main


def change_plexi_thickness(file_dir, width):
    """
    Change specific part of geo.dat (thickness of plexi)
    """
    tmp_file, tmp_path = mkstemp()
    with fdopen(tmp_file, 'w') as new_file:
        with open(join(file_dir, 'geo.dat')) as old_file:
            geo = old_file.readlines()
            tmp = geo[6].strip('\n').strip('\r')
            geo[6] = tmp[:-8] + '{:01.6f}'.format(width) + '\n'
            for line in geo:
                new_file.write(line)
    remove(join(file_dir, 'geo.dat'))
    move(tmp_path, join(file_dir, 'geo.dat'))


if __name__ == '__main__':
    directory = sys.argv[1]
    plexi_file = sys.argv[2]
    with open(plexi_file, 'r') as plx_f:
        thickness_list = plx_f.readlines()

    for th in thickness_list:
        th = float(th)
        curr = th / 10.0  # presumably file contains data in [mm] from pbc.optimizer, shield uses [cm]
        print("Creating geo.dat for thickness {0}".format(curr))
        change_plexi_thickness(directory, curr)

        print('{0} starting!'.format(th))
        time.sleep(0.5)
        main([str(directory), '-j', '10', '-p', '1000000', '-b', 'slurm', '-s', '[ --time=90]'])
        time.sleep(1)  # date with seconds is used in directory name, so sleep after each execution
        print('{0} finished!'.format(th))
