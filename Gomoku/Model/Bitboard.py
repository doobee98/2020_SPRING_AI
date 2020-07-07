from enum import Enum, auto
from typing import Tuple, Dict


class Vec(Enum):
    Row = auto()        # (1, 0)
    Col = auto()        # (0, 1)
    DiagUp = auto()     # (1, 1)
    DiagDown = auto()   # (1, -1)


"""
Bitboard
한 색상의 보드 정보를 담는 클래스이다.
Shift 연산을 처리하기 위한 Padding인 Margin을 추가하여, 
19*(19+8)개의 비트로 보드를 표시한다.
"""
class Bitboard:
    # Type Decision
    B = int
    P = Tuple[int, int]

    # class invariants
    Size = 19
    Margin = 8
    Total = Size + Margin
    Full = int(('0'*Margin + '1'*Size)*Size, 2)
    Empty = 0b0
    Shift = {
        Vec.Row: 1,
        Vec.Col: Total,
        Vec.DiagUp: Total - 1,
        Vec.DiagDown: Total + 1
    }

    def __init__(self, value: int = Empty):
        self.__board = value
        self.__count = bin(self.__board).count('1')

    """
    property
    * board
    """
    def board(self) -> B:
        return self.__board

    """
    advanced property
    * item
    * count
    """
    def hasItem(self, pos: P) -> bool:
        return bool(self.__board & self.pos2mask(pos))

    def setItem(self, pos: P, value: bool) -> None:
        if value:
            self.__board |= self.pos2mask(pos)
            self.__count += 1
        else:
            self.__board &= ~self.pos2mask(pos)
            self.__count -= 1

    def count(self) -> int:
        return self.__count

    """
    operation
    * and, or, invert, int, bool, eq, ne, lshift, rshift
    * dilation
    * erosion
    """
    def __and__(self, other) -> 'Bitboard':
        return Bitboard(self.board() & int(other))

    def __or__(self, other) -> 'Bitboard':
        return Bitboard(self.board() | int(other))

    def __invert__(self) -> 'Bitboard':
        return Bitboard(~self.board())

    def __int__(self):
        return self.board()

    def __bool__(self):
        return self.board() != Bitboard.Empty

    def __eq__(self, other) -> bool:
        return self.board() == int(other)

    def __ne__(self, other) -> bool:
        return self.board() != int(other)

    def __lshift__(self, other) -> 'Bitboard':
        return self.board() << other

    def __rshift__(self, other) -> 'Bitboard':
        return self.board() >> other

    def dilation(self, value: int) -> 'Bitboard':
        # 팽창, 현재 보드에서 모든 vec으로 value만큼 간 위치를 추가하여 반환함.
        result = self.__board
        for vec_iter in Vec:
            shift_iter = Bitboard.Shift[vec_iter]
            result |= self.__board << (shift_iter * value)
            result |= self.__board >> (shift_iter * value)
        return Bitboard(result & Bitboard.Full)
        
    def erosion(self, value: int) -> 'Bitboard':
        # 침식, 현재 보드에서 모든 vec으로 value만큼 줄어든 보드를 반환함
        result = self.__board
        for vec_iter in Vec:
            shift_iter = Bitboard.Shift[vec_iter]
            result &= self.__board << (shift_iter * value)
            result &= self.__board >> (shift_iter * value)
        return Bitboard(result & Bitboard.Full)
    
    """
    method
    * copySelf
    * lineQuery
    * matchLineQuery
    """
    def copySelf(self) -> 'Bitboard':
        return Bitboard(self.__board)

    def lineQuery(self, line_query: int, line_length: int, vec: Vec) -> 'Bitboard':
        # 해당 line query가 해당 방향(vec)으로 board에 존재하면 그 위치를 반환함
        neg_board = ~self.__board
        query_iter = line_query
        bits_iter = self.__board if query_iter & 1 else neg_board
        for idx_iter in range(1, line_length):
            query_iter >>= 1
            bits_iter = (self.__board if query_iter & 1 else neg_board) & (bits_iter << Bitboard.Shift[vec])
            if bits_iter == 0:
                break
        return Bitboard(bits_iter & Bitboard.Full)

    def matchLineQuery(self, query_result: 'Bitboard', line_query: int, line_length: int, vec: Vec) -> 'Bitboard':
        # line query의 매칭된 보드 모양을 반환함
        if query_result == Bitboard.Empty:
            return query_result
        else:
            query_iter = line_query
            bits_iter = query_result if query_iter & 1 else 0
            for idx_iter in range(1, line_length):
                query_iter >>= 1
                bits_iter = (query_result if query_iter & 1 else 0) | (bits_iter >> Bitboard.Shift[vec])
            return Bitboard(bits_iter)

    """
    class method
    * pos2idx
    * pos2mask
    * idx2pos
    """
    @classmethod
    def pos2idx(cls, pos: P) -> int:
        return pos[0] * cls.Total + pos[1]

    @classmethod
    def pos2mask(cls, pos: P) -> B:
        return 1 << cls.pos2idx(pos)

    @classmethod
    def idx2pos(cls, idx: int) -> P:
        return idx // cls.Total, idx % cls.Total

    """
    debug method
    * printBoard
    """
    def printBoard(self) -> None:
        board_temp = self.__board
        line_masking = (1 << Bitboard.Size) - 1
        for row_iter in range(Bitboard.Size):
            print(f'{bin(line_masking & board_temp):0>21}')
            board_temp >>= Bitboard.Total
        print()
