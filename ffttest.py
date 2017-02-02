from numpy.core.numeric import arange
import schrpy as sch
import scipy as sp
from scipy.sparse.linalg import eigs
from time import time
pot = sch.us_KP_potential(8, 5, 0.4)
x = sp.arange(-60, 60, 0.05)
xo = sch.gaussian(0, 1, 1).func
hamil = sch.schroedinger(pot, xo).hamiltonian
t = time()
eig = eigs(hamil, k=1200)
print(time()-t)
sp.save('eigen.npy', eig)