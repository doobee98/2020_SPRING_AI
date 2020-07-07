from Strategy.ChooseStrategy import *


# 게임 플레이어
class Player:
    def __init__(self, name: str, is_ai: bool, time_limit: int = 10):
        self.__name = name
        self.__time_limit = time_limit  # 시간제한, 초단위
        self.__is_ai = is_ai
        self.__strategy: ChooseStrategy = None  # 행동결정 strategy, player strategy는 구현이 제대로 되지 않음.

    """
    property
    * isAI
    * name
    * timeLimit
    * strategy
    """
    def isAI(self) -> bool:
        return self.__is_ai

    def setAI(self, is_ai: bool) -> None:
        self.__is_ai = is_ai

    def name(self) -> str:
        return self.__name

    def setName(self, name: str) -> None:
        self.__name = name

    def timeLimit(self) -> int:
        return self.__time_limit

    def setTimeLimit(self, time_limit: int) -> None:
        self.__time_limit = time_limit

    def strategy(self) -> ChooseStrategy:
        return self.__strategy

    def setStrategy(self, strategy: ChooseStrategy) -> None:
        self.__strategy = strategy

    """
    advanced property
    * isValid
    """
    def isValid(self) -> bool:
        return self.__time_limit > 0
