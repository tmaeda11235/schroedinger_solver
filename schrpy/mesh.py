from scipy import arange, meshgrid


class mesh:

    def __init__(self, xmin=-60, xmax=60, dx=0.02, t0=0, tmax=20, dt=0.02):
        self.xmin = xmin
        self.xmax = xmax
        self.dx = dx
        self.t0 = t0
        self.tmax = tmax
        self.dt = dt

        self.x = arange(self.xmin, self.xmax, self.dx)
        self.t = arange(self.t0, self.tmax, self.dt)
        self.xlen = len(self.x)
        self.tlen = len(self.t)
        self.x2d, self.t2d = meshgrid(self.x, self.t)
        self.dense = (self.dx ** -1, self.dt ** -1)

    def __str__(self):
        xstr = "{}<x<{}  (dx={})".format(self.xmin, self.xmax, self.dt)
        tstr = "{}<t<{}  (dt={})".format(self.t0, self.tmax, self.dx)
        return "{}  &  {}".format(xstr, tstr)

    def __add__(self, other):
        if self.dense != other.dense:
            raise(ValueError("To add two schrpy.mesh, they should have same dense. "))
        elif not self.overWrapped(other):
            raise(ValueError("To add two schrpy.mesh, they should have overwapped-zone. "))

        else:
            newxmin = min(self.xmin, other.xmin)
            newxmax = max(self.xmax, other.xmax)
            newt0 = min(self.t0, other.t0)
            newtmax = max(self.tmax, other.tmax)
            return mesh(xmin=newxmin, xmax=newxmax, dx=self.dx, t0=newt0, tmax=newtmax, dt=self.dt)

    def overWrapped(self, other):
        if other.xmax < self.xmin or self.xmax < other.xmin:
            return False
        elif other.tmax < self.t0 or self.tmax < other.t0:
            return False

        else:
            return True
