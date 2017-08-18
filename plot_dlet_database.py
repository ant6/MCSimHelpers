import matplotlib.pyplot as plt
import numpy as np
from beprof import profile
import os

data_sets = {}
profiles = []
values = []

files = os.listdir('.')
dose_data_files = []
dletg_data_files = []

positions, weights = np.loadtxt("result.dat", delimiter=";", usecols=(0, 1), unpack=True)
print("Positions:\n%s\nWeights:\n%s" % (positions, weights))
weights = weights[::-1]

for fd in files:
    if "mm.dat" in fd:
        dose_data_files.append(fd)
print("Dose data files:\n%s" % dose_data_files)

for ff in files:
    if "mm-dletg.dat" in ff:
        dletg_data_files.append(ff)
print("DLETG data files:\n%s" % dletg_data_files)

for idx, datafile in enumerate(dose_data_files):
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

dose_sum = sum(values)
plt.plot(tmp_prof.x, dose_sum)

plt.xlim([0, 18])
plt.title("Monte Carlo modulator sim (r15 m15)")
plt.xlabel("Depth in water [mm]")
plt.ylabel("Relative dose")
plt.show()

print(dose_sum.max(), dose_sum.min())

# error_lim = dose_sum.max() / 1000
# print("Allowed error: %s" % error_lim)
# bool_mask = dose_sum > error_lim
# bool_mask = bool_mask.astype(np.int)
# print("Boolean mask:")
# print(bool_mask)
# print("Bool mask length: %s" % len(bool_mask))

dletg_data_sets = {}
dletg_profiles = []
dletg_values = []

for dletg_idx, dletg_datafile in enumerate(dletg_data_files):
    print("\nFile {0}:".format(dletg_datafile))
    dletg_name = dletg_datafile.strip('.dat')
    dletg_range = dletg_datafile.strip('mm-dletg.dat')
    dletg_range = float(dletg_range) * 10
    print("Processing data for: %s [mm]" % dletg_range)

    dletg_data_sets[dletg_name] = np.loadtxt(dletg_datafile)

    print("Max = ", dletg_data_sets[dletg_name][:, 1].max())
    dletg_data_sets[dletg_name][:, 1] /= dletg_data_sets[dletg_name][:, 1].max()

    DS = data_sets[dletg_name.strip('-dletg')][:, 1]
    dletg_data_sets[dletg_name][:, 1] = np.multiply(dletg_data_sets[dletg_name][:, 1],
                                                    (DS > 0.001 * DS.max()).astype(np.int))

    dletg_data_sets[dletg_name][:, 0] *= 10

    tmp_prof = profile.Profile(dletg_data_sets[dletg_name][:, :2])
    dletg_profiles.append(tmp_prof)

    # plt.plot(tmp_prof.x, tmp_prof.y * weights[dletg_idx], 'b')
    # plt.show()

    dletg_values.append(tmp_prof.y)  # * weights[dletg_idx])


dletg_sum = np.zeros(350)
for let_idx, let_peak in enumerate(dletg_values):
    dletg_sum += weights[let_idx] * let_peak

dletg_sum /= sum(weights)

plt.plot(tmp_prof.x, dletg_sum, 'r')

plt.xlim([0, 35])

plt.title("Symulacja modulatora r15 m15 (DLETG)")
plt.xlabel("Zasięg w wodzie [mm]")
plt.ylabel("DLETG")
plt.show()
