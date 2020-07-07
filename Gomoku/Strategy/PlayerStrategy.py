from Strategy.ChooseStrategy import *
from PyQt5.QtCore import pyqtSlot, pyqtBoundSignal


"""
PlayerStrategy
User의 의사선택 과정을 구현함. BoardView에서 입력을 받아서 처리한다.
"""
class PlayerStrategy(ChooseStrategy):
    def __init__(self, color: Color, select_signal: pyqtBoundSignal):
        super().__init__(color)
        self.select_signal = select_signal

    """
    inherited method
    * isActive
    * start
    * stop
    """
    def isActive(self) -> bool:
        return self.timer.isActive()

    def start(self, board: GameBoard, second_limit: int) -> None:
        self.timer.start(second_limit)
        self.select_signal.connect(self.squareSelected)
        self.Started.emit()

    def restart(self, board: GameBoard) -> None:
        self.timer.start()
        self.select_signal.connect(self.squareSelected)
        self.Started.emit()

    def stop(self) -> None:
        self.timer.stop()
        self.select_signal.disconnect(self.squareSelected)
        self.Finished.emit()

    """
    slot
    * squareSelected
    """
    @pyqtSlot(tuple)
    def squareSelected(self, pos: Bitboard.P):
        self.setDecision(pos)
        self.stop()
