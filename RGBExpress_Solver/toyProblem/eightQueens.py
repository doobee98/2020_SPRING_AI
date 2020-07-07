from problem import *
from typing import Tuple

N = 8


class BoardState(State):
    def __init__(self, board: str):
        super().__init__()
        self.__board = board

    def board(self) -> str:
        return self.__board

    def nextRow(self) -> int:
        for idx, c in enumerate(self.board()):
            if c == '0':
                return idx + 1
        return 0

    def setQueen(self, next_col: int) -> None:
        b = self.__board
        next_row = self.nextRow() - 1
        if next_row < 0:
            raise ValueError
        self.__board = b[:next_row] + str(next_col) + b[(next_row + 1):]


class BoardAction(Action):
    def __init__(self, nextCol: int):
        self.__next = nextCol

    def value(self) -> int:
        return self.__next


def boardActions(state: BoardState) -> List[Action]:
    action_list = []
    next_row_idx = state.board().find('0')
    if next_row_idx == -1:
        return []

    for y in range(1, N + 1):
        # check before queens
        flag = True
        for idx_iter in range(next_row_idx + 1):
            row_idx_iter = next_row_idx - idx_iter
            c = int(state.board()[row_idx_iter])
            if c == y or c == y - idx_iter or c == y + idx_iter:
                flag = False
                break
        if flag:
            action_list.append(BoardAction(y))

    return action_list


def boardTrans(state: BoardState, action: BoardAction) -> BoardState:
    new_state = BoardState(state.board())
    next_col = action.value()
    new_state.setQueen(next_col)
    return new_state


def boardGoalTest(state: BoardState) -> bool:
    return state.board().count('0') == 0


def boardActionCost(state: BoardState, action: BoardAction) -> int:
    return 1


eightQueenProblem = Problem(
    BoardState('0'*N),         # initial state
    boardActions,                       # actions
    boardTrans,                         # transition model
    boardGoalTest,                      # goal test
    boardActionCost                     # action cost
)

