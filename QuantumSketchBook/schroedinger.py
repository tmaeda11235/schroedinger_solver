from QuantumSketchBook.state import State
from scipy import zeros
from scipy.integrate import ode


class Schroedinger:

    def __init__(self, hamiltonian, x0state: State):
        self.mesh = hamiltonian.mesh
        self._operator = -1j * hamiltonian.matrix()
        self.x0state = x0state

        self.ode = ode(self.equation)
        self.ode.set_integrator('zvode', nsteps=1000000)
        self.ode.set_initial_value(self.x0state.vector)

    def equation(self, t, phi0):
        return self._operator.dot(phi0)

    def generator(self):
        yield self.x0state.vector
        index = 1
        print("now solving", end=" ")
        while self.ode.successful() and index < self.mesh.t_num:
            fin = (index + 1) / self.mesh.t_num
            print('\rSchrodinger have solved {:3.2%}! '.format(fin), end=' ' if not fin == 1 else "\n", flush=True)
            yield self.ode.integrate(self.mesh.t_vector[index])
            index += 1

    def solution(self):
        sol = zeros([self.mesh.t_num, self.mesh.x_num], dtype=complex)
        for i, s in enumerate(self.generator()):
            sol[i] = s
        while True:
            yield sol
