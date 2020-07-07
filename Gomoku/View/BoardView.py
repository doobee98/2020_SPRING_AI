from Model.GameBoardOrderExtension import *
from Model.Notation import *
from typing import Tuple
from PyQt5.QtWidgets import QWidget, QGridLayout, QLayout
from PyQt5.QtGui import QPalette, QPixmap, QBrush
from PyQt5.QtCore import pyqtSlot
from View.SquareView import *


"""
BoardView
게임 보드 전체를 표현하는 클래스.
보드 판 각각의 칸을 SquereView 클래스 리스트를 통해 관리함.
"""
class BoardView(QWidget):
    SquareDoubleClicked = pyqtSignal(tuple)
    SquareEnter = pyqtSignal(tuple)
    SquareLeave = pyqtSignal(tuple)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.square_list: List[List[SquareView]] = [[None for _ in range(Bitboard.Size)] for _ in range(Bitboard.Size)]
        self.is_show_order = False

        # Square View 설정 (HitBox Spacing and assign)
        gbox = QGridLayout()
        gbox.setContentsMargins(6, 6, 6, 6)
        gbox.setSpacing(6)
        for row_iter in range(Bitboard.Size):
            for col_iter in range(Bitboard.Size):
                square_widget = SquareView()
                square_widget.DoubleClicked.connect(self.squareDoubleClicked)
                square_widget.MouseEnter.connect(self.squareEntered)
                square_widget.MouseLeave.connect(self.squareLeaved)
                gbox.addWidget(square_widget, row_iter, col_iter)
                self.square_list[row_iter][col_iter] = square_widget
        self.setLayout(gbox)

        # set size and background checkerboard
        self.setFixedSize(600, 600)
        pixmap = QPixmap('img/checkerboard.png').scaled(600, 600, Qt.IgnoreAspectRatio)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    """
    property
    * squareView
    """
    def squareView(self, pos: Bitboard.P) -> SquareView:
        row, col = pos
        return self.square_list[row][col]

    """
    method
    * draw, drawSquare
    """
    def draw(self, model: GameBoardOrderExtension) -> None:
        # total draw
        for row_iter in range(Bitboard.Size):
            for col_iter in range(Bitboard.Size):
                self.drawSquare(model, (row_iter, col_iter))

    def drawSquare(self, model: GameBoardOrderExtension, pos: Bitboard.P) -> None:
        sqr, order = model.item(pos), model.order(pos)
        sqr_view = self.squareView(pos)
        sqr_view.draw(sqr)
        if self.is_show_order and sqr != None:
            sqr_view.setText(str(order))

    """
    slot
    * squareDoubleClicked
    * squareEntered
    * squareLeaved
    """
    @pyqtSlot()
    def squareDoubleClicked(self) -> None:
        sqr: SquareView = self.sender()
        if sqr:
            for row_iter in range(Bitboard.Size):
                for col_iter in range(Bitboard.Size):
                    if sqr == self.squareView((row_iter, col_iter)):
                        self.SquareDoubleClicked.emit((row_iter, col_iter))
                        return

    @pyqtSlot()
    def squareEntered(self) -> None:
        sqr: SquareView = self.sender()
        if sqr:
            for row_iter in range(Bitboard.Size):
                for col_iter in range(Bitboard.Size):
                    if sqr == self.squareView((row_iter, col_iter)):
                        self.SquareEnter.emit((row_iter, col_iter))
                        return

    @pyqtSlot()
    def squareLeaved(self) -> None:
        sqr: SquareView = self.sender()
        if sqr:
            for row_iter in range(Bitboard.Size):
                for col_iter in range(Bitboard.Size):
                    if sqr == self.squareView((row_iter, col_iter)):
                        self.SquareLeave.emit((row_iter, col_iter))
                        return

    """
    class method
    * pos2note, note2pos
    * _row_pos2note, _row_note2pos, _col_pos2note, _col_note2pos
    """
    @classmethod
    def pos2note(cls, pos: Tuple[int, int]) -> str:
        return cls._row_pos2note(pos[0]) + cls._col_pos2note(pos[1])

    @classmethod
    def note2pos(cls, note: str) -> Tuple[int, int]:
        note_row, note_col = note[0:1], note[1:]
        return cls._row_note2pos(note_row), cls._col_note2pos(note_col)

    @classmethod
    def _row_pos2note(cls, pos_row: int) -> str:
        return chr(pos_row + ord('A'))

    @classmethod
    def _row_note2pos(cls, note_row: str) -> int:
        return ord(note_row) - ord('A')

    @classmethod
    def _col_pos2note(cls, pos_col: int) -> str:
        return str(pos_col + 1)

    @classmethod
    def _col_note2pos(cls, note_col: str) -> int:
        return int(note_col) - 1

