from typing import Callable, List, Optional
from enum import Enum, auto


class Action:
    def value(self):
        raise NotImplementedError


class State:
    def __lt__(self, other):
        return True


class Problem:
    def __init__(self,
                 initial_state: State,
                 actions: Callable[[State], List[Action]],
                 transition_model: Callable[[State, Action], State],
                 goal_test: Callable[[State], bool],
                 path_cost: Callable[[State, Action], int]):
        self.__initial_state = initial_state
        self.__actions = actions
        self.__transition_model = transition_model
        self.__goal_test = goal_test
        self.__path_cost = path_cost

    """
    problem methods
    * initialState
    * actions
    * doAction
    * isGoalState
    * pathCost
    """
    def initialState(self) -> State:
        return self.__initial_state

    def actions(self, state: State) -> List[Action]:
        return self.__actions(state)

    def doAction(self, state: State, action: Action) -> State:
        return self.__transition_model(state, action)

    def isGoalState(self, state: State) -> bool:
        return self.__goal_test(state)

    def pathCost(self, state: State, action: Action) -> int:
        return self.__path_cost(state, action)
