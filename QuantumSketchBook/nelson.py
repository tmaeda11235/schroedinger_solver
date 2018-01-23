from typing import TYPE_CHECKING
from scipy import imag, real, log, sqrt, random, zeros
from scipy.interpolate import RectBivariateSpline
if TYPE_CHECKING:
    from QuantumSketchBook.schroedinger import Schroedinger


class Nelson:
    def __init__(self, schroedinger: "Schroedinger", n: int, micro_steps=10):
        self.mesh = schroedinger.mesh
        psi = schroedinger.solution()
        imz, rez = imag(log(psi)), real(log(psi))
        self.realSpline = RectBivariateSpline(self.mesh.t_vector, self.mesh.x_vector, rez)
        self.imagSpline = RectBivariateSpline(self.mesh.t_vector, self.mesh.x_vector, imz)
        self.x = schroedinger.x0state.random_values(n)
        self.t = self.mesh.t_min
        self.n = n
        self.t_micro = self.mesh.dt / micro_steps
        self.micro_steps = micro_steps

    def drift(self, x, t):
        re = self.realSpline.ev(t, x, dy=1)
        im = self.imagSpline.ev(t, x, dy=1)
        return re + im

    def run(self):
        rand = sqrt(0.5) * random.normal(scale=sqrt(self.t_micro), size=self.n)
        self.x += self.drift(self.x, self.t) * self.t_micro + rand
        self.t += self.t_micro
        return self.x

    def set_t(self, new_t):
        self.t = new_t
        return self

    def locus(self):
        locus_array = zeros((self.n, self.mesh.t_num))
        locus_array[:, 0] = self.x
        for i in range(1, self.mesh.t_num):
            print("\rNelson have solved {:.2%}!".format(i / self.mesh.t_num), end=" ", flush=True)
            for j in range(self.micro_steps-1):
                self.run()
            locus_array[:, i] = self.run()
        print("\rNelson have solved 100.00%!", flush=True)
        return locus_array
