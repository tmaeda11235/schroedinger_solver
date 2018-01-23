from QuantumSketchBook.field import Field
from QuantumSketchBook.context import MeshContext
from scipy.stats import norm
from scipy import array, exp, absolute, ones, random


class State(Field):

    def random_values(self, n):
        probability = absolute(self.vector) ** 2
        probability = probability * 10000  # 有効数字を3ケタ以上取るために10000倍する
        probability_naturalized = probability.astype(int)
        target = []
        for i in range(self.mesh.x_num):
            weight = probability_naturalized[i]
            if not weight == 0:
                weight_array = i * ones(weight, dtype=int)
                target.extend(weight_array.tolist())
        max_random = len(target)
        target_index = random.randint(0, max_random, n)
        random_index = array(target)[target_index]
        return self.mesh.x_vector[random_index]

    def __plot__(self, show, save, title, *args, **kwargs):
        super().__plot__(show, save, title, "probability", absolute(self.vector) ** 2)


def gaussian_state(mean, sd, wave_number):
    x = MeshContext.get_mesh().x_vector
    pdf = norm.pdf(x, mean, sd / 2)
    wav = exp(1j * wave_number * x)
    return State(array(pdf * wav, dtype=complex))


if __name__ == "__main__":
    import QuantumSketchBook as QSB
    with QSB.Context(0, 10, 1, 0, 10, 1):
        test1 = absolute(gaussian_state(5, 1, 0).vector)
        assert max(test1) == test1[5]
        assert test1[4] == test1[6]
        QSB.plot(gaussian_state(0, 3, 1), False, True)
