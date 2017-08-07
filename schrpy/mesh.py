from scipy import arange, meshgrid


class Mesh:

    def __init__(self, x_min, x_max, dx, t_min, t_max, dt):
        self.x_min = x_min
        self.x_max = x_max
        self.dx = dx
        self.t_min = t_min
        self.t_max = t_max
        self.dt = dt
        self.param = (x_min, x_max, dx, t_min, t_max, dt)

        self.x_vector = arange(x_min, x_max, dx)
        self.t_vector = arange(t_min, t_max, dt)
        self.x_num = len(self.x_vector)
        self.t_num = len(self.t_vector)
        self.x_matrix, self.t_matrix = meshgrid(self.x_vector, self.t_vector)
        self.dense = (self.dx ** -1, self.dt ** -1)

    def __str__(self):
        x_string = "{}<x<{}  (dx={})".format(self.x_min, self.x_max, self.dt)
        t_string = "{}<t<{}  (dt={})".format(self.t_min, self.t_max, self.dx)
        return "{}\n{}".format(x_string, t_string)

    def __eq__(self, other):
        return self.param == other.param


class MyMesh(Mesh):

    def __init__(self, x_min=-60, x_max=60, dx=0.02, t_min=0, t_max=20, dt=0.02):
        super(MyMesh, self).__init__(x_min, x_max, dx, t_min, t_max, dt)

