from QuantumSketchBook import *
from scipy import array, absolute, save
import matplotlib.pyplot as plt
mesh = Mesh(-10**4, 10**4, 1, 0, 10**4, 1)
t = mesh.t_vector
x2 = mesh.x_vector**2
plt.figure(figsize=(10, 10))
for v in (0, 1, 1.5, 1.9, 2):
    pot = potential(mesh, array([v*(-1)**x if -50<=x<=50 else 0 for x in mesh.x_vector]))
    hamil = Hamiltonian(mesh, pot, mass=0.5, boundary="poor")
    state = State(mesh, array([1 if x==0 else 0 for x in mesh.x_vector]))
    schroedinger = hamil.schroedinger(state).generator()
    var = array([(x2 * absolute(phi)**2).sum() for phi in schroedinger])
    plt.loglog(t[1:], var[1:], lw=5)
    save("zhang{}.npy".format(v), var)

plt.xlim(2, 10 ** 4)
plt.ylim(0.2, 10**8)
plt.title("Reproducing Zhang's graph")
plt.savefig("zhang.png")
