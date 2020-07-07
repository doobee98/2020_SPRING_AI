from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from Model.Player import *


class PlayerView(QGroupBox):
    def __init__(self, is_left: bool, parent: QWidget = None):
        super().__init__(parent)

        self.name_lbl = QLabel('Player')
        self.name_lbl.setAlignment(Qt.AlignCenter)
        title_font = self.name_lbl.font()
        title_font.setPointSize(15)
        title_font.setBold(True)
        self.name_lbl.setFont(title_font)

        self.count_lbl = QLabel('30s')
        self.count_lbl.setAlignment(Qt.AlignCenter)
        count_font = self.count_lbl.font()
        count_font.setPointSize(20)
        count_font.setBold(True)
        self.count_lbl.setFont(count_font)

        w1, w2 = (self.name_lbl, self.count_lbl) if is_left else (self.count_lbl, self.name_lbl)
        hbox = QHBoxLayout()
        hbox.addWidget(w1)
        hbox.addWidget(w2)
        self.setLayout(hbox)

    def draw(self, model: Player):
        self.name_lbl.setText(model.name())
        self.setCount(model.timeLimit())

    def highlight(self) -> None:
        self.setStyleSheet('background-color: white')

    def dehighlight(self) -> None:
        self.setStyleSheet('')

    def setCount(self, count: int) -> None:
        self.count_lbl.setText(f'{count:0>2}')