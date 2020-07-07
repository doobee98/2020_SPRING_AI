from PyQt5.QtWidgets import QGroupBox, QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimerEvent, Qt
from typing import Optional


"""
AlertView
쌍삼, 좌표 등의 정보를 표시하는 클래스
"""
class AlertView(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.lbl = QLabel(' ')
        self.lbl.setAlignment(Qt.AlignCenter)
        lbl_font = self.lbl.font()
        lbl_font.setPointSize(25)
        lbl_font.setBold(True)
        self.lbl.setFont(lbl_font)
        self.timer_id: Optional[int] = None

        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl)
        self.setLayout(hbox)
        
    """
    method
    * alert
    * clear
    """
    def alert(self, text: str, count: int = 2000) -> None:
        # count 시간 만큼 alertView에 text를 띄움
        self.clear()
        self.lbl.setText(text)
        self.timer_id = self.startTimer(count)

    def clear(self) -> None:
        self.lbl.setText('')
        if self.timer_id is not None:
            self.killTimer(self.timer_id)
            self.timer_id = None

    """
    slot
    * timerEvent
    """
    def timerEvent(self, event: 'QTimerEvent') -> None:
        super().timerEvent(event)
        self.clear()
