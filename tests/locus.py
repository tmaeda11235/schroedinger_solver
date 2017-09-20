from scipy import *
from matplotlib.pyplot import *

locus = load("double_well_locus.npy")

n = zeros(2000)
for j in range(60):
    for i in range(2000):
        time_slice = locus[i]
        n[i] = size(where(absolute(time_slice - j) < 2))

    plot(arange(0, 200, 0.1), n)
    yscale("log")
    savefig("reflection{}.png".format(j))
    clf()