from typing import List
from nptyping import NDArray, Float64
from src.types.state import STATE


"""
HMM
* hmm model class (parsed from hmmParser)
"""
class HMM:
    def __init__(self, name: str, tp: NDArray[Float64], state_list: List[STATE]):
        self.name = name
        self.tp = tp
        self.states = state_list
