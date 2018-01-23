from typing import Any, Iterable, Union, NamedTuple, Sequence, Callable, Iterator
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

    @abstractmethod
    def x_vector(self) -> NDArray:
        pass

    @abstractmethod
    def t_vector(self) -> NDArray:
        pass

    @abstractmethod
    def x_num(self) -> int:
        return len(self.x_vector)

    @abstractmethod
    def t_num(self) -> int:
        return len(self.x_vector)

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass


class Context:

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


class Quantized:

    @abstractmethod
    def update_mesh(self) -> None:
        pass


class Field:

    @abstractmethod
    def __init__(self, arg: Union[NDArray, Callable], mesh: Mesh) -> None:
        pass

    @abstractmethod
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

