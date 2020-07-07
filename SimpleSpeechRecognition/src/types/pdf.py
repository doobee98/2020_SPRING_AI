from nptyping import NDArray, Float64


N_DIMENSION = 39
N_PDF = 2
N_STATE = 3
TYPE_VECTOR = NDArray[N_DIMENSION, Float64]


"""
PDF
* pdf model class (parsed from hmmParser)
"""
class PDF:
    def __init__(self, w: Float64, m: TYPE_VECTOR, v: TYPE_VECTOR):
        self.weight = w
        self.median = m
        self.variance = v
