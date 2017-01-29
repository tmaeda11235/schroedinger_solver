from scipy import arange, array
from scipy.sparse import dia_matrix, csr_matrix


class laplasian(object):

    def __init__(self, dx):
        self.dx = dx

    def matrix(self, x):
        length = len(x)
        det = array(1 / (360 * self.dx ** 2))
        coef = array([[4], [-54], [540], [-980], [540], [-54], [4]])
        std = det * coef
        data = std.repeat(length + 1, axis=1)
        pad = arange(-3, 4)
        dia = dia_matrix((data, pad), shape=(length, length))
        csr = dia.tocsr()
        fix = csr.data
        bound = array([-440, 486, -50, 4, 486, -976, 540, -54, 4, -50]) * det
        fix[:10] = bound
        fix[-10:] = bound[::-1]
        fixed = csr_matrix((fix, csr.indices, csr.indptr), dtype=complex)
        return fixed