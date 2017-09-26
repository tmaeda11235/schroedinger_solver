from QuantumSketchBook.mesh import Mesh


class MeshContextError(ValueError):
    pass


class MeshContext:

    _has_mesh = False
    _mesh = None
    _context = None
    _followers = set()

    def __new__(cls, mesh=None):
        if not cls._has_mesh:
            if isinstance(mesh, Mesh):
                cls._has_mesh = True
                cls._mesh = mesh
                cls._context = super().__new__(cls)
            else:
                raise MeshContextError("invalid argument {} should ({})".format(mesh.__class__, Mesh.__class__))
        return cls._context

    @classmethod
    def get_mesh(cls):
        if cls._mesh is not None:
            return cls._mesh
        else:
            raise MeshContextError("not found mesh in context")

    @classmethod
    def update_mesh(cls, mesh):
        if isinstance(mesh, Mesh):
            cls._mesh = mesh
        for follower in cls._followers:
            follower.update_mesh()
        return cls()

    @classmethod
    def has_instance(cls):
        return cls._has_mesh

    @classmethod
    def clean(cls):
        cls._mesh = None
        cls._context = None
        cls._has_mesh = False
        return None

    @classmethod
    def add_follower(cls, follower):
        if hasattr(follower, "update_mesh"):
            cls._followers.add(follower)
        else:
            raise ValueError("follower should have update_mesh(). ")

    @classmethod
    def remove_follower(cls, follower):
        if follower in cls._followers:
            cls._followers.discard(follower)
        else:
            raise ValueError("{} is not follower. ".format(follower))

    @classmethod
    def is_follower(cls, item):
        return item in cls._followers


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
