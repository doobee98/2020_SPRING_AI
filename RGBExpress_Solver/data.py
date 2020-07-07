from toyProblem.routeFinding import *
from toyProblem.eightQueens import *
from mainProblem.rgbexpress import *
from mainProblem.parse import *
from mainProblem.testcases import *


class Data:
    __INSTANCE = None
    @classmethod
    def __instance(cls) -> 'Data':
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    def __init__(self):
        self.__data_dict = {}
        self.__data_dict['Route-Finding'] = routeProblem
        self.__data_dict['8-Queens'] = eightQueenProblem
        for key, data in rgb_testcases.items():
            self.__data_dict[f'RGB-Express {key}'] = createRGBExpressProblem(parseInitialState(data))

    @classmethod
    def problem(cls, code: str) -> Problem:
        return cls.__instance().__data_dict[code]