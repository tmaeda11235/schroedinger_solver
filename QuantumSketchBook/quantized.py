from QuantumSketchBook.context import MeshContext


class Quantized:
    def __init__(self, mesh=None):
        if mesh is not None:
            self.mesh = mesh
        else:
            self.mesh = MeshContext.get_mesh()
            MeshContext.add_observer(self)

    def update_mesh(self):
        self.mesh = MeshContext.get_mesh()


if __name__ == "__main__":
    mod = __import__("QuantumSketchBook.mesh")
    mesh1 = mod.my_mesh()
    mesh2 = mod.my_mesh(x_min=0)
    MeshContext(mesh1)
    a = Quantized()
    assert a.mesh == mesh1

    MeshContext.update_mesh(mesh2)
    assert Quantized().mesh == mesh2
    assert not a.mesh == mesh1
    assert a.mesh == mesh2
