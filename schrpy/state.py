from scipy.stats import norm
from scipy import array, exp


class gaussian:

    def __init__(self, mean, sd, wavenumber):
        self.mean = mean
        self.sd = sd
        self.wavenumber = wavenumber

    def func(self, x):
        pdf = array(norm.pdf(x, self.mean, self.sd), dtype=complex)
        wav = exp(-1j * self.wavenumber * x)
        return pdf * wav
