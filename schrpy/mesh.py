from scipy import arange, meshgrid


class Mesh:

    def __init__(self, xmin, xmax, dx, t0, tmax, dt):
        self.xmin = xmin
        self.xmax = xmax
        self.dx = dx
        self.t0 = t0
        self.tmax = tmax
        self.dt = dt
        self.param = (xmin, xmax, dx, t0, tmax, dt)

        self.x_vector = arange(xmin, xmax, dx)
        self.t_vector = arange(t0, tmax, dt)
        self.x_num = len(self.x_vector)
        self.t_num = len(self.t_vector)
        self.x_matrix, self.t_matrix = meshgrid(self.x_vector, self.t_vector)
        self.dense = (self.dx ** -1, self.dt ** -1)

    def __str__(self):
        x_string = "{}<x<{}  (dx={})".format(self.xmin, self.xmax, self.dt)
        t_string = "{}<t<{}  (dt={})".format(self.t0, self.tmax, self.dx)
        return "{}\n{}".format(x_string, t_string)

    def __eq__(self, other):
        return self.param == other.param


class MyMesh(Mesh):

    def __init__(self, xmin=-60, xmax=60, dx=0.02, t0=0, tmax=20, dt=0.02):
        super(MyMesh, self).__init__(xmin, xmax, dx, t0, tmax, dt)
