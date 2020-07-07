from Model.GameBoard import *
from Model.Rule import *
from PyQt5.QtCore import QObject, pyqtSignal, QTimer


"""
ChooseStrategy
의사 결정 함수를 strategy 패턴으로 구현함
"""
class ChooseStrategy(QObject):
    Started = pyqtSignal()
    Finished = pyqtSignal()

    def __init__(self, color: Color):
        super().__init__()
        self.__decision: Tuple[Optional[int], Optional[int]] = (None, None)
        self.color = color
        self.timer: QTimer = QTimer()

    """
    property
    * decision
    """
    def decision(self) -> Bitboard.P:
        return self.__decision

    def setDecision(self, pos: Bitboard.P) -> None:
        self.__decision = pos

    """
    method
    * isActive
    * start
    * restart
    * stop
    * choose
    """
    def isActive(self) -> bool:
        pass

    def start(self, board: GameBoard, second_limit: int) -> None:
        pass

    def restart(self, board: GameBoard) -> None:
        pass

    def stop(self) -> None:
        pass
    
    # finished 신호에 맞춰 외부에서 호출되며, 결정된 decision을 return함
    def choose(self) -> Optional[Bitboard.P]:
        if self.isActive():
            self.stop()
        row, col = self.decision()
        if row is None or col is None:
            return None
        else:
            return self.decision()
