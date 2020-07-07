from Model.GameBoard import *
from typing import List


"""
GameBoardOrderExtension
View에서 보드에 돌을 둔 순서를 보여주기 위해 필요한 GameBoard Decorator
"""
class GameBoardOrderExtension(GameBoard):
    def __init__(self):
        super().__init__()
        self.__order_board: List[List[int]] = [[0 for _ in range(Bitboard.Size)] for _ in range(Bitboard.Size)]

    def orderBoard(self) -> List[List[int]]:
        return self.__order_board

    def order(self, pos: Bitboard.P) -> int:
        return self.__order_board[pos[0]][pos[1]]

    def setItem(self, pos: Bitboard.P, item: Square) -> None:
        super().setItem(pos, item)
        row, col = pos
        if item is not None:
            self.__order_board[row][col] = self.count()
        else:
            self.__order_board[row][col] = 0
