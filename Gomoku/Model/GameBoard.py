from Model.Bitboard import *
from Model.LineQuery import LineQuery
from typing import Optional


class Color(Enum):
    Black = auto()
    White = auto()
    def opponent(self) -> 'Color':
        return Color.Black if self == Color.White else Color.White


Square = Optional[Color]


"""
GameBoard
Bitboard 2개로 각각의 색상의 돌의 배치 상태를 나타냄으로서
오목 게임 보드를 모델링한다.
추가적으로 최근 액션인 lastAction을 property로 가지며
LineQuery 클래스를 이용하여 쿼리를 판정할 수 있다.
"""
class GameBoard:
    def __init__(self, other: 'GameBoard' = None):
        if other is None:
            self.__color_board: Dict[Color, Bitboard] = {
                Color.Black: Bitboard(),
                Color.White: Bitboard()
            }
            self.__last_action: Tuple[int, int] = (None, None)
        else:
            self.__color_board = { color: other.colorBoard(color).copySelf() for color in Color }
            self.__last_action: Tuple[int, int] = other.lastAction()

    """
    property
    * colorBoard
    * lastAction
    """
    def colorBoard(self, color: Color) -> Bitboard:
        return self.__color_board[color]

    def lastAction(self) -> Tuple[int, int]:
        return self.__last_action

    """
    advanced property
    * totalBoard
    * count
    * item
    """
    def totalBoard(self) -> Bitboard:
        return self.colorBoard(Color.Black) | self.colorBoard(Color.White)

    def count(self) -> int:
        return self.colorBoard(Color.Black).count() + self.colorBoard(Color.White).count()

    def item(self, pos: Bitboard.P) -> Square:
        if self.colorBoard(Color.Black).hasItem(pos):
            return Color.Black
        elif self.colorBoard(Color.White).hasItem(pos):
            return Color.White
        else:
            return None

    def setItem(self, pos: Bitboard.P, item: Square) -> None:
        row, col = pos
        self.colorBoard(item).setItem(pos, True)
        self.__last_action = (row, col)

    """
    method
    * copySelf
    * isFull
    * lineQueryCount, lineQueryResult, lineQueryResultWithPattern
    """
    def copySelf(self) -> 'GameBoard':
        return GameBoard(self)

    def isFull(self) -> bool:
        return self.count() >= Bitboard.Size * Bitboard.Size

    # 보드 내 해당 Query의 개수를 반환한다.
    def lineQueryCount(self, current: Color, line_query: LineQuery) -> count:
        # current color의 입장에서 line query를 찾은 개수를 반환함
        count = 0
        result_dict = self.lineQueryResult(current, line_query)
        for vec_iter in Vec:
            if result_dict[vec_iter]:  # 해당 쿼리가 보드 내부에 존재함
                count += bin(result_dict[vec_iter].board()).count('1')  ##### 더 나은게 없을까?
        return count

    # 보드 내 해당 Query의 위치를 Vec과 묶어서 반환한다.
    def lineQueryResult(self, current: Color, line_query: LineQuery) -> Dict[Vec, 'Bitboard']:
        my_board, op_board = self.colorBoard(current), self.colorBoard(current.opponent())
        result = {}
        for vec_iter in Vec:
            my_result = my_board.lineQuery(line_query.myQuery(), line_query.length(), vec_iter)
            op_result = op_board.lineQuery(line_query.opQuery(), line_query.length(), vec_iter)
            result[vec_iter] = my_result & op_result
        return result

    # 보드 내 해당 Query의 위치와, 해당 Query를 보드판에 표현한 보드를 Vec과 묶어서 반환한다.
    def lineQueryResultWithPattern(self, current: Color, line_query: LineQuery) -> Dict[Vec, Tuple['Bitboard', 'Bitboard']]:
        result_dict = {}
        my_board, my_query = self.colorBoard(current), line_query.myQuery()
        length = line_query.length()
        query_result_dict = self.lineQueryResult(current, line_query)
        for vec_iter, query_result_iter in query_result_dict.items():
            my_ptn = my_board.matchLineQuery(query_result_iter, my_query, length, vec_iter)
            result_dict[vec_iter] = (query_result_iter, my_ptn)
        return result_dict

    """
    debug method
    * printBoard
    """
    def printBoard(self) -> None:
        for row_iter in range(Bitboard.Size):
            print(f'{row_iter:>2}', end='')
            for col_iter in range(Bitboard.Size):
                item_iter = self.item((row_iter, col_iter))
                if item_iter == Color.Black:
                    print('●', end='')
                elif item_iter == Color.White:
                    print('○', end='')
                else:
                    print('┼', end='')
            print()



