from nptyping import Float64
from typing import List
import numpy as np
from src.types.pdf import N_DIMENSION, TYPE_VECTOR


"""
SingleGaussian
* simple multivariate gaussian distribution
"""
class SingleGaussian:
    def __init__(self, m: TYPE_VECTOR, v: TYPE_VECTOR):
        self.__median = m
        self.__var = v

        # computed
        self.__bottom = np.power(np.pi * 2, N_DIMENSION/2) * np.prod(np.sqrt(v))

    def probability(self, x: TYPE_VECTOR) -> Float64:
        top = np.sum([np.power(x[i] - self.__median[i], 2) / self.__var[i] for i in range(N_DIMENSION)])
        return np.exp(-0.5 * top) / self.__bottom


"""
MultiGaussian
* composition of multi singleGaussian distributions with their weights
"""
class MultiGaussian:
    def __init__(self, weightList: List[Float64], sgdList: List[SingleGaussian]):
        assert len(weightList) == len(sgdList)
        self.__weight_list = weightList
        self.__sgd_list = sgdList

    def probability(self, x: TYPE_VECTOR) -> Float64:
        return np.sum([self.__weight_list[i] * self.__sgd_list[i].probability(x)
                       for i in range(len(self.__weight_list))])
