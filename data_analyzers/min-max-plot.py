import os
import matplotlib.pyplot as plt
import numpy as np


def find_nearest(array, value):
    i = (np.abs(array-value)).argmin()
    return i

plt.plot([0, 25], [1.01, 1.01], 'g-')
plt.plot([0, 25], [1.0, 1.0], 'y-')
plt.plot([0, 25], [0.99, 0.99], 'g-')

min_dom = []
min_val = []

max_dom = []
max_val = []

for ff in os.listdir('.'):
    if '-iter_' in ff:
        idx = ff.split("-")[0]
        data = np.loadtxt(os.path.join(ff, 'plateau_zoom.dat'), delimiter=";", unpack=True)
        lower_bound = find_nearest(data[0], 0)
        upper_bound = find_nearest(data[0], 27.9)  # cut the falling to 0.9 edge
        # print(lower_bound, upper_bound)
        # print(data[0][lower_bound], data[0][upper_bound])

        min_dom.append(idx)
        min_val.append(data[1][lower_bound:upper_bound].min())
        # plt.plot(idx, data[1][lower_bound:upper_bound].min(), 'bo')
        print("X pos for %s" % data[1][lower_bound:upper_bound].min())
        print(data[0][data[1][lower_bound:upper_bound].argmin()])
        max_dom.append(idx)
        max_val.append(data[1][lower_bound:upper_bound].max())
        # plt.plot(idx, data[1][lower_bound:upper_bound].max(), 'ro')
        # plt.plot(data[0][lower_bound:upper_bound], data[1][lower_bound:upper_bound])

plt.plot(min_dom, min_val, 'bo', label="min")
plt.plot(max_dom, max_val, 'ro', label="max")
fig = plt.gcf()
fig.set_size_inches(8, 6)

plt.legend()
plt.xlabel("Liczba iteracji")
plt.ylabel("Relatywna dawka")
plt.show()
