from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Strategy.Search import *


"""
SearchView
AI의 의사 결정 과정을 간략하게 표시함.
"""
class SearchView(QTextEdit):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFontPointSize(12)

    """
    slot
    * updateSearch
    """
    @pyqtSlot(int, tuple, int)
    def updateSearch(self, depth: int, action: Bitboard.P, value: int) -> None:
        self.append(f'Depth {depth}: {action} / {value}\n')
