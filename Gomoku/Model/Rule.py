from Model.GameBoard import *
from typing import Optional


class Rule:
    # 싱글턴 패턴
    _INSTANCE = None
    @classmethod
    def _getInstance(cls) -> 'Rule':
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def __init__(self):
        self.name = 'Custom'
        three_str_list =  ['__OOO__', 'X_OOO__', '__OOO_X', '__OO_O__', 'X_OO_O__', '__OO_O_X', 'X_OO_O_X',
                           '__O_OO__', 'X_O_OO__', '__O_OO_X', 'X_O_OO_X']
        win_str_list = ['_OOOOO_', 'XOOOOO_', '_OOOOOX', 'XOOOOOX']
        self.__three_query = [LineQuery(str) for str in three_str_list]
        self.__win_query = [LineQuery(str) for str in win_str_list]

    @classmethod
    def isAble(cls, board: GameBoard, color: Color, pos: Bitboard.P) -> bool:
        # 쌍삼 불가능
        done_state = board.copySelf()
        done_state.setItem(pos, color)
        return not cls.checkDoubleThree(done_state, color)

    @classmethod
    def checkWin(cls, board: GameBoard) -> Optional[Color]:
        # 정확히 오목을 완성한 플레이어가 있으면 승리함
        if board.isFull():
            return None  # 무승부
        for color_iter in Color:
            for query_iter in cls._getInstance().__win_query:
                if board.lineQueryCount(color_iter, query_iter) != 0:
                    return color_iter
        return None  # 진행중

    # 쌍삼 체크
    @classmethod
    def checkDoubleThree(cls, board: GameBoard, color: Color) -> bool:
        # 만약 win이면 바로 False 리턴
        if cls.checkWin(board) is not None:
            return False
        last_action_mask = Bitboard.pos2mask(board.lastAction())

        # 3이 있는 곳의 패턴을 Bitboard로 리스트에 넣음
        pattern3_list = []
        for query_iter in cls._getInstance().__three_query:
            ptn_result = board.lineQueryResultWithPattern(color, query_iter)
            for vec_iter, (_, query_pattern_iter) in ptn_result.items():
                if query_pattern_iter != Bitboard.Empty:
                    pattern3_list.append(query_pattern_iter)

        # 리스트 안에 있는 3끼리 모두 pair 해서 and 해보고, 겹치는 곳이 있으면 return
        count = len(pattern3_list)
        for i in range(count - 1):
            for j in range(i + 1, count):
                if pattern3_list[i] & pattern3_list[j] & last_action_mask:
                    return True
        return False

    """
    class method
    * isPosValid, isRowValid, isColValid
    """
    @classmethod
    def isPosValid(cls, row: int, col: int) -> bool:
        return Rule.isRowValid(row) and Rule.isColValid(col)

    @classmethod
    def isRowValid(cls, row: int) -> bool:
        return 0 <= row < Bitboard.Size

    @classmethod
    def isColValid(cls, col: int) -> bool:
        return 0 <= col < Bitboard.Size

Rule._getInstance()
