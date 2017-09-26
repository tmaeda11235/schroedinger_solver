from QuantumSketchBook.field import Field
from QuantumSketchBook.context import MeshContext
from scipy.stats import norm
from scipy import array, exp, absolute, ones, random


class State(Field):

    def random_values(self, n):
        probability = absolute(self.vector()) ** 2
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


def state(arg):
    mesh = MeshContext.get_mesh()
    return State(mesh, arg)


def gaussian_state(mean, sd, wave_number):
    x = MeshContext.get_mesh().x_vector
    pdf = norm.pdf(x, mean, sd / 2)
    wav = exp(1j * wave_number * x)
    return State(array(pdf * wav, dtype=complex))
