from typing import Any, Generic, Iterable, Union, NamedTuple, Sequence, Callable, Iterator
from numbers import Real, Number
from abc import abstractmethod
from scipy.sparse import csr_matrix


NDArray = Sequence[Number]
X_Min = Real
X_Max = Real
Dx = Real
T_Min = Real
T_Max = Real
Dt = Real


class Mesh(NamedTuple):
    x_min: X_Min
    x_max: X_Max
    dx: Dx
    t_min: T_Min
    t_max: T_Max
    dt: Dt

    @property
    @abstractmethod
    def x_vector(self) -> NDArray:
        pass

    @property
    @abstractmethod
    def t_vector(self) -> NDArray:
        pass

    @property
    @abstractmethod
    def x_num(self) -> int:
        return len(self.x_vector)

    @property
    @abstractmethod
    def t_num(self) -> int:
        return len(self.x_vector)

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass


class Context(Generic[X_Min, X_Max, Dx, T_Min, T_Max, Dt]):

    @abstractmethod
    def __new__(cls, x_min: X_Min, x_max: X_Max, dx: Dx,
                t_min: T_Min, t_max: T_Max, dt: Dt) -> "Context":
        pass

    @abstractmethod
    def __enter__(self) -> Mesh:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        pass


class Quantized(Generic[Any, Mesh]):

    @abstractmethod
    def update_mesh(self) -> None:
        pass


class Field(Quantized[Union[NDArray, Callable], Mesh]):

    @abstractmethod
    def __init__(self, arg: Union[NDArray, Callable], mesh: Mesh) -> None:
        pass

    @abstractmethod
    @property
    def vector(self) -> NDArray:
        pass


class Potential(Field):

    @abstractmethod
    def matrix(self) -> csr_matrix:
        pass


class State(Field):

    @abstractmethod
    def random_generator(self) -> Iterator[Real]:
        pass


class Solver(Iterable[NDArray]):

    @abstractmethod
    def __init__(self, args: Any) -> None:
        pass

    @abstractmethod
    def __iter__(self) -> NDArray:
        pass


Hamiltonian = Quantized[Potential, Mesh]


class Dynamic(Iterable[Field]):

    @abstractmethod
    def __init__(self, args: Union[Callable, Iterable[Iterable]]):
        pass

    @abstractmethod
    def __iter__(self):
        pass
