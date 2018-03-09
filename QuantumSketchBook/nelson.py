from typing import TYPE_CHECKING
from scipy import imag, real, log, sqrt, random, zeros
from scipy.interpolate import CubicSpline
if TYPE_CHECKING:
    from QuantumSketchBook.schroedinger import Schroedinger


class Nelson:
    def __init__(self, schroedinger: "Schroedinger", n: int, micro_steps=10):
        self.schroedinger = schroedinger
        self.mesh = schroedinger.mesh
        self.x = schroedinger.x0state.random_values(n)
        self.n = n
        self.t_micro = self.schroedinger.mesh.dt / micro_steps
        self.micro_steps = micro_steps

    def derivative_fo_part(self, part, sch):
        log_part = part(log(sch))
        spline = CubicSpline(self.mesh.x_vector, log_part)
        return spline(self.x, 1)

    def run(self, drift):
        for _ in range(self.micro_steps):
            rand = sqrt(0.5) * random.normal(scale=sqrt(self.t_micro), size=self.n)
            self.x += drift(self.x) * self.t_micro + rand
        return self.x

    def locus(self):
        locus_array = zeros((self.n, self.mesh.t_num))
        locus_array[:, 0] = self.x
        for i in range(1, self.mesh.t_num):
            for j in range(self.micro_steps-1):
                self.run()
            locus_array[:, i] = self.run()
        print("\rNelson have solved 100.00%!", flush=True)
        return locus_array

    def __iter__(self):
        self.x = self.schroedinger.x0state.random_values(self.n)
        yield self.x
        for i, sch in enumerate(self.schroedinger):
            drift = self.derivative_fo_part(real, sch) + self.derivative_fo_part(imag, sch)
            yield self.run(drift)
            print(f"\rNelson have solved {(i + 1) / self.mesh.t_num:.2%}!", end=" ", flush=True)
