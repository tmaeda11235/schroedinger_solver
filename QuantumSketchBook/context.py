from QuantumSketchBook.mesh import Mesh


class MeshContextError(ValueError):
    pass


class MeshContext:

    _has_mesh = False
    _mesh = None
    _context = None
    _observer = list()
    _in_context = False

    def __new__(cls, mesh=None):
        if not cls._has_mesh:
            if cls._in_context:
                raise MeshContextError("MeshContext should not be over written in 'with block'. ")

            if isinstance(mesh, Mesh):
                cls._has_mesh = True
                cls.update_mesh(mesh)
                cls._context = super().__new__(cls)
            else:
                raise MeshContextError("invalid argument {} should ({})".format(mesh.__class__, Mesh.__class__))
        return cls._context

    @classmethod
    def get_mesh(cls):
        if cls._mesh is not None:
            return cls._mesh
        else:
            raise MeshContextError("not found any mesh in Context")

    @classmethod
    def update_mesh(cls, mesh):
        if isinstance(mesh, Mesh):
            cls._mesh = mesh
        for osv in cls._observer:
            osv.update_mesh()
        return cls()

    @classmethod
    def has_instance(cls):
        return cls._has_mesh

    @classmethod
    def clean(cls):
        cls._has_mesh = False
        cls._mesh = None
        cls._context = None
        cls._observer = list()

    @classmethod
    def add_observer(cls, observer):
        if hasattr(observer, "update_mesh"):
            cls._observer.append(observer)
        else:
            raise ValueError("observer should have the update_mesh(). ")

    @classmethod
    def remove_observer(cls, observer):
        if observer in cls._observer:
            cls._observer.remove(observer)
        else:
            raise ValueError("{} is not a observer of MeshContext. ".format(observer))

    @classmethod
    def is_observer(cls, item):
        return item in cls._observer

    @classmethod
    def set_context_on(cls):
        cls._in_context = True

    @classmethod
    def set_context_off(cls):
        cls._in_context = False


class Context:

    def __init__(self, x_min, x_max, dx, t_min, t_max, dt):
        self.mesh = Mesh(x_min, x_max, dx, t_min, t_max, dt)
        self._pre_mesh = None
        self._pre_observer = list()

    def __enter__(self):
        if MeshContext.has_instance():
            self._pre_mesh = MeshContext.get_mesh()
        MeshContext(self.mesh)
        MeshContext.set_context_on()
        return self.mesh

    def __exit__(self, exc_type, vallue, traceback):
        MeshContext().set_context_off()
        MeshContext.clean()
        if self._pre_mesh is not None:
            MeshContext(self._pre_mesh)


if __name__ == "__main__":
    mesh1 = Mesh(-10, 10, 1, 0, 10, 1)
    mesh2 = Mesh(0, 10, 1, 0, 10, 1)
    a = MeshContext(mesh1)
    assert a.has_instance()
    assert a.get_mesh() == mesh1

    b = MeshContext()
    assert a.get_mesh() == b.get_mesh()
    assert a is b

    c = MeshContext.update_mesh(mesh2)
    assert a.get_mesh() == c.get_mesh()
    assert a is c

    MeshContext.clean()
    assert not a.has_instance()

    try:
        a.get_mesh()
        error = False
    except MeshContextError:
        error = True
    assert error

    def error_check(*args):
        try:
            MeshContext(*args)
        except MeshContextError:
            return True
        return False

    assert error_check()
    assert error_check(3)
    assert not error_check(mesh2)
    MeshContext().clean()
    with Context(-10, 0, 1, -10, 0, 1) as mm:
        assert mm == Mesh(-10, 0, 1, -10, 0, 1)

    try:
        MeshContext.get_mesh()
    except MeshContextError as e:
        assert e.args[0] == "not found any mesh in Context"
