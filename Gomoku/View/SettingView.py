from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Model.GameBoard import Color
from Model.Player import *
from typing import Tuple


"""
SettingView
게임 시작 전, 사전에 제한 시간, 이름, 돌 가리기 등 
게임에 필요한 정보를 입력받는 Dialog 클래스이다.
"""
class SettingView(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        player_default: Tuple[str, int] = ('Player', 60)
        ai_default: Tuple[str, int] = ('AI', 10)

        self.black_player = Player(player_default[0], False)
        self.white_player = Player(player_default[0], False)
        player_view_list = []
        hbox = QHBoxLayout()

        for color_iter in Color:
            group = QGroupBox('BLACK' if color_iter == Color.Black else 'WHITE')

            player_button = QRadioButton('Player')
            ai_button = QRadioButton('AI')
            button_group = QButtonGroup()
            button_group.addButton(player_button, 0)
            button_group.addButton(ai_button, 1)

            name_lbl = QLabel('  이름  : ')
            name_le = QLineEdit()
            count_lbl = QLabel('제한시간: ')
            count_le = QLineEdit()
            count_le.setValidator(QIntValidator(1, 999))  # 999 까지만 입력 가능
            player_view_list.append((button_group, name_le, count_le))

            player_button.clicked.connect(lambda _, le=name_le: le.setText(player_default[0]))
            player_button.clicked.connect(lambda _, le=count_le: le.setText(str(player_default[1])))
            ai_button.clicked.connect(lambda _, le=name_le: le.setText(ai_default[0]))
            ai_button.clicked.connect(lambda _, le=count_le: le.setText(str(ai_default[1])))
            if color_iter == Color.Black:
                player_button.click()
            else:
                ai_button.click()

            button_box = QHBoxLayout()
            button_box.addWidget(player_button)
            button_box.addWidget(ai_button)

            gbox = QGridLayout()
            gbox.addWidget(name_lbl, 0, 0)
            gbox.addWidget(name_le, 0, 1)
            gbox.addWidget(count_lbl, 1, 0)
            gbox.addWidget(count_le, 1, 1)

            group_box = QVBoxLayout()
            group_box.addLayout(button_box)
            group_box.addLayout(gbox)
            group.setLayout(group_box)
            hbox.addWidget(group)

        accept_button = QPushButton('확인')
        accept_button.clicked.connect(lambda: self.black_player.setAI(player_view_list[0][0].button(1).isChecked()))
        accept_button.clicked.connect(lambda: self.black_player.setName(player_view_list[0][1].text()))
        accept_button.clicked.connect(lambda: self.black_player.setTimeLimit(int(player_view_list[0][2].text())))
        accept_button.clicked.connect(lambda: self.white_player.setAI(player_view_list[1][0].button(1).isChecked()))
        accept_button.clicked.connect(lambda: self.white_player.setName(player_view_list[1][1].text()))
        accept_button.clicked.connect(lambda: self.white_player.setTimeLimit(int(player_view_list[1][2].text())))
        accept_button.clicked.connect(self.accept)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(accept_button)

        self.setLayout(vbox)
        self.setWindowTitle('Setting')
