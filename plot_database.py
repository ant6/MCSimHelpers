import matplotlib.pyplot as plt
import numpy as np
from beprof import profile
import os

data_sets = {}
profiles = []
values = []

files = os.listdir('.')
plot_data_files = []

positions, weights = np.loadtxt("result.dat", delimiter=";", usecols=(0, 1), unpack=True)
print(positions, weights)
weights = weights[::-1]

for ff in files:
    if "mm.dat" in ff:
        plot_data_files.append(ff)
print(plot_data_files)

idx = 0

for datafile in plot_data_files:
    print("\nFile {0}:".format(datafile))
    dose_name = datafile.strip('.dat')
    dose_range = datafile.strip('mm.dat')
    dose_range = float(dose_range) * 10
    print("Processing data for: %s [mm]" % dose_range)

    data_sets[dose_name] = np.loadtxt(datafile)
    
    print("Max = ", data_sets[dose_name][:, 1].max())
    data_sets[dose_name][:, 1] /= data_sets[dose_name][:, 1].max()
    data_sets[dose_name][:, 0] *= 10

    tmp_prof = profile.Profile(data_sets[dose_name][:, :2])
    profiles.append(tmp_prof)

    plt.plot(tmp_prof.x, tmp_prof.y * weights[idx])

    values.append(tmp_prof.y * weights[idx])
    idx += 1

tmp_sum = sum(values)
plt.plot(tmp_prof.x, tmp_sum)

plt.xlim([0, 16])

plt.title("Symulacja modulatora r15 m15")
plt.xlabel("Zasięg w wodzie [mm]")
plt.ylabel("Relatywna dawka")
plt.show()
