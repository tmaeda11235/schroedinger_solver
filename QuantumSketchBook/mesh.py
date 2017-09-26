from scipy import arange
from numbers import Real
from collections import namedtuple


class Mesh(namedtuple("_Mesh", "x_min, x_max, dx, t_min, t_max, dt")):

    def __new__(cls, x_min, x_max, dx, t_min, t_max, dt):
        if not all(isinstance(x, Real) for x in (x_min, x_max, dx, t_min, t_max, dt)):
            raise TypeError("input should be a number")
        if not (x_min < x_max and t_min < t_max):
            raise ValueError("The min should be smaller than The max. ")
        if not (0 < dx or 0 < dt):
            raise ValueError("The dx and dt should be positive. ")
        if not (x_max - x_min > dx and t_max - t_min > dt):
            raise ValueError("too big to make mesh. ")
        return super().__new__(cls, x_min, x_max, dx, t_min, t_max, dt)

    @property
    def param(self):
        return self.x_min, self.x_max, self.dx, self.t_min, self.t_max, self.dt

    @property
    def x_vector(self):
        return arange(self.x_min, self.x_max, self.dx)

    @property
    def t_vector(self):
        return arange(self.t_min, self.t_max, self.dt)

    @property
    def x_num(self):
        return len(self.x_vector)

    @property
    def t_num(self):
        return len(self.t_vector)

    @property
    def dense(self):
        return self.dx ** -1, self.dt ** -1

    def __str__(self):
        x_string = "{}<x<{}  (dx={})".format(self.x_min, self.x_max, self.dt)
        t_string = "{}<t<{}  (dt={})".format(self.t_min, self.t_max, self.dx)
        return "\n".join((x_string, t_string))

    def __eq__(self, other):
        return self.param == other.param


def my_mesh(x_min=-10, x_max=10, dx=0.1, t_min=0, t_max=10, dt=0.1):
    return Mesh(x_min, x_max, dx, t_min, t_max, dt)

if __name__ == "__main__":
    print(my_mesh())