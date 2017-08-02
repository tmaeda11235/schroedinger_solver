from scipy import arange, meshgrid


class mesh:

    def __init__(self, xmin=-60, xmax=60, dx=0.02, t0=0, tmax=20, dt=0.02):
        self.xmin = xmin
        self.xmax = xmax
        self.dx = dx
        self.t0 = t0
        self.tmax = tmax
        self.dt = dt

        self.x_vector = arange(self.xmin, self.xmax, self.dx)
        self.t_vector = arange(self.t0, self.tmax, self.dt)
        self.x_num = len(self.x_vector)
        self.t_num = len(self.t_vector)
        self.x_matrix, self.t_matrix = meshgrid(self.x_vector, self.t_vector)
        self.dense = (self.dx ** -1, self.dt ** -1)

    def __str__(self):
        xstr = "{}<x<{}  (dx={})".format(self.xmin, self.xmax, self.dt)
        tstr = "{}<t<{}  (dt={})".format(self.t0, self.tmax, self.dx)
        return "{}  &  {}".format(xstr, tstr)
