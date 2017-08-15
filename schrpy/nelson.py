from scipy import imag, real, log, sqrt, random, zeros
from scipy.interpolate import RectBivariateSpline


class Nelson:
    def __init__(self, mesh, psi, x_init, run_times=10):
        imz, rez = imag(log(psi)), real(log(psi))
        self.realSpline = RectBivariateSpline(mesh.t_vector, mesh.x_vector, rez)
        self.imagSpline = RectBivariateSpline(mesh.t_vector, mesh.x_vector, imz)
        self.t = mesh.t_min
        self.dt = mesh.dt
        self.t_num = mesh.t_num
        self.x = x_init
        self.n = len(x_init)
        self.t_micro = mesh.dt / run_times
        self.run_times = run_times

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
        locus_array = zeros((self.n, self.t_num))
        locus_array[:, 0] = self.x
        for i in range(1, self.t_num):
            print("\rNelson {}% done ! now".format(int(100 * i / self.t_num)), end=" ", flush=True)
            for j in range(self.run_times-1):
                self.run()
            locus_array[:, i] = self.run()
        return locus_array
