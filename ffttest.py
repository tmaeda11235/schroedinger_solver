from numpy.core.numeric import arange
import schrpy as sch
import scipy as sp
from scipy.sparse.linalg import eigs
from time import time
pot = sch.us_KP_potential(8., 5., 1.)
xo = sch.gaussian(0., 1., 1.).func
hamil = sch.schroedinger(pot, xo, dx=0.001).hamiltonian
t = time()
val, vec = eigs(hamil, k=1000)
print(time()-t)
sp.save('eigenvec.npy', vec)
sp.save('eigenval.npy', val)