import scipy as sp


class laplasian(object):

    def __init__(self, dx):
        self.dx = dx

    def matrix(self, x):
        length = len(x)
        det = sp.array(1 / (360 * self.delta ** 2), dtype=complex)
        coef = sp.array([[4], [-54], [540], [-980], [540], [-54], [4]])
        std = det * coef
        data = std.repeat(length + 1, axis=1)
        pad = sp.arange(-3, 4)
        dia = sp.sparse.dia_matrix((data, pad), shape=(length, length))
        csr = dia.tocsr()
        return csr
