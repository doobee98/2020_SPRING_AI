from PyQt5.QtWidgets import QWidget,  QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QMouseEvent
from Model.GameBoard import Color, Square


"""
SquareView
보드 각각의 판을 표시하는 View.
User와의 interaction signal을 발생시키며, 각 칸의 상태를 렌더링한다.
"""
class SquareView(QLabel):
    DoubleClicked = pyqtSignal()
    MouseEnter = pyqtSignal()
    MouseLeave = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setText(' ')
        self.setAlignment(Qt.AlignCenter)

    """
    method
    * draw
    """
    def draw(self, model: Square) -> None:
        self.setText(' ')
        if model is None:
            self.setStyleSheet('background-color: rgba(0, 0, 0, 0);')
        elif model == Color.Black:
            self.setStyleSheet('background-color: rgba(0, 0, 0, 0);'
                               'color: rgba(255, 255, 255, 255);'
                               'border-image: url(./img/black_stone.png);')
        else:
            self.setStyleSheet('background-color: rgba(0, 0, 0, 0);'
                               'color: rgba(0, 0, 0, 255);'
                               'border-image: url(./img/white_stone.png);')

    """
    event
    * mouseDoubleClickEvent
    * enterEvent, leaveEvent
    """
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)
        self.DoubleClicked.emit()

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.MouseEnter.emit()

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self.MouseLeave.emit()
