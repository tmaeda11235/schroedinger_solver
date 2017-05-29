from scipy import imag, real, log, sqrt, random
from scipy.interpolate import RectBivariateSpline


class nelson:
    def __init__(self, x, t, psi, x_init):
        imz, rez = imag(log(psi)), real(log(psi))
        self.realSpline, self.imagSpline = RectBivariateSpline(t, x, rez), RectBivariateSpline(t, x, imz)
        self.t = 0
        self.x = x_init
        self.n = len(x_init)

    def drift(self, x, t):
        re = self.realSpline.ev(t, x, dx=1)
        im = self.imagSpline.ev(t, x, dx=1)
        return (re + im)/2

    def run(self, dt):
        rand = sqrt(0.5) * random.normal(scale=dt, size=self.n)
        self.x += self.drift(self.x, self.t) * dt + rand
        self.t += dt
        return self.x

    def setT(self, newT):
        self.t = newT
        return self