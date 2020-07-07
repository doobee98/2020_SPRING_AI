# from Model.GameBoard import Color
from typing import Tuple


class LineQuery:
    def __init__(self, query: str):
        if query is not None:
            (self.__my_query, self.__op_query, self.__length) = LineQuery.__parseStringQuery(query)
        else:  # null initializer for copy
            self.__my_query, self.__op_query, self.__length = 0, 0, 0

    """
    property
    * myQuery, opQuery
    * length
    """
    def myQuery(self) -> int:
        return self.__my_query

    def opQuery(self) -> int:
        return self.__op_query

    def length(self) -> int:
        return self.__length

    """
    method
    * copyOpponent
    * printQuery
    """
    def copyOpponent(self) -> 'LineQuery':
        new_query = LineQuery(None)
        new_query.__my_query = self.__op_query
        new_query.__op_query = self.__my_query
        new_query.__length = self.__length
        return new_query

    """
    class method
    * parseStringQuery
    """
    @classmethod
    def __parseStringQuery(cls, query: str) -> Tuple[int, int, int]:
        my_line, op_line = 0b0, 0b0
        for c in query:
            my_line <<= 1
            op_line <<= 1
            if c == 'O':
                my_line |= 0b1
            elif c == 'X':
                op_line |= 0b1
        return my_line, op_line, len(query)

    """
    debug method
    * printQuery
    """
    def printQuery(self) -> None:
        my_iter, op_iter = self.myQuery(), self.opQuery()
        result = ''
        for _ in range(self.length()):
            if my_iter & 1:
                result += '0'
            elif op_iter & 1:
                result += 'X'
            else:
                result += '_'
            my_iter >>= 1
            op_iter >>= 1
        print(result)