from typing import List, Optional
from Model.GameBoard import Color


# 기보
class Notation:
    def __init__(self):
        self.note_list: List[List[str]] = []
        self.__current_color: Color = None   # 현재 대기중인(두어야하는) 플레이어 색상을 나타냄

    def addNote(self, note: str) -> None:
        # 첫 수 예외처리
        if self.__current_color is None:
            self.__current_color = Color.Black

        if self.__current_color == Color.Black:
            self.note_list.append([note])
            self.__current_color = Color.White
        else:
            self.note_list[-1].append(note)
            self.__current_color = Color.Black

    def peekNote(self) -> Optional[str]:
        if self.__current_color == Color.White:
            return self.note_list[-1][0]
        elif self.__current_color == Color.Black:
            return self.note_list[-1][1]
        else:
            return None

    def popNote(self) -> Optional[str]:
        if self.__current_color == Color.White:
            note = self.note_list[-1][0]
            del self.note_list[-1]
            if len(self.note_list) == 0:
                self.__current_color = None
            else:
                self.__current_color = Color.Black
        elif self.__current_color == Color.Black:
            note = self.note_list[-1][1]
            del self.note_list[-1][1]
            self.__current_color = Color.White
        else:
            note = None
        return note

