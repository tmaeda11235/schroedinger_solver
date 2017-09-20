from numpy.core.numeric import arange
import schrpy as sch
import scipy as sp
from scipy.sparse.linalg import eigs
from time import time
pot = sch.potential(lambda x: 0.5 * x ** 2 + 1000 * (sp.absolute(x) > 9.9))
#pot = sch.us_KP_potential(6.5, 4, 1)
xo = sch.gaussian(0., 3., 2.).func
hamil = sch.schroedinger(pot, xo, dx=0.01, xmin=-10, xmax=10).hamiltonian
t = time()
val, vec = eigs(hamil, k=30, which='SM')
print(time()-t)
#sp.save('eigvec.npy', vec[:, sp.argsort(val)])
#sp.save('eigval.npy', sp.sort(val))
sp.save('HarmonicVec.npy', vec[:, sp.argsort(val)])
sp.save('HarmonicVal.npy', sp.sort(val))
