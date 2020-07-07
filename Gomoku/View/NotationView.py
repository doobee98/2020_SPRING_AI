from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Model.Notation import *


"""
NotationView
기보를 화면에 표시함
"""
class NotationView(QTextEdit):
    MouseEnter = pyqtSignal()
    MouseLeave = pyqtSignal()

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFontFamily('Courier New')
        self.setFontPointSize(15)

    """
    method
    * draw
    """
    def draw(self, model: Notation) -> None:
        note_string = 'Black  White\n------------\n'
        for row_notes_iter in model.note_list:
            note_string += f' {row_notes_iter[0]:<3} '
            if len(row_notes_iter) > 1:
                note_string += f'   {row_notes_iter[1]:<3} '
            note_string += '\n'
        self.setText(note_string)

    """
    event
    * enterEvent, leaveEvent
    """
    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.MouseEnter.emit()

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self.MouseLeave.emit()