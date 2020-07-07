from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Model.GameBoardOrderExtension import *
from Model.Player import *
from Model.Rule import *
from Model.Notation import *
from View.BoardView import *
from View.PlayerView import *
from View.NotationView import *
from View.AlertView import *
from View.SearchView import *
from Strategy.PlayerStrategy import *
from Strategy.AIStrategy import *
from typing import Dict


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.board_model = GameBoardOrderExtension()
        self.notation_model = Notation()
        self.player_model: Dict[Color, Player] = {Color.Black: None, Color.White: None}

        self.board_view = BoardView()
        self.notation_view = NotationView()
        self.player_view = {
            Color.Black: PlayerView(True),
            Color.White: PlayerView(False)
        }
        self.alert_view = AlertView()
        self.search_view = SearchView()

        self.timer_count = 30000  # default, it will be changed by player
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.secondOut)
        self.current_turn: Color = Color.Black
        
        # connect signal
        # self.board_view.SquareDoubleClicked.connect(self.squareSelected)
        self.board_view.SquareEnter.connect(self.squareEntered)
        self.board_view.SquareLeave.connect(self.squareLeaved)
        self.notation_view.MouseEnter.connect(self.showBoardOrder)
        self.notation_view.MouseLeave.connect(self.hideBoardOrder)

        # 레이아웃 구성
        hbox_top = QHBoxLayout()
        hbox_top.addWidget(self.player_view[Color.Black])
        hbox_top.addWidget(self.alert_view)
        hbox_top.addWidget(self.player_view[Color.White])

        vbox_right = QVBoxLayout()
        vbox_right.addWidget(self.notation_view)

        vbox_left = QVBoxLayout()
        vbox_left.addLayout(hbox_top)
        vbox_left.addWidget(self.board_view)

        hbox_total = QHBoxLayout()
        hbox_total.addLayout(vbox_left)
        hbox_total.addLayout(vbox_right)
        hbox_total.addWidget(self.search_view)

        central = QWidget()
        central.setLayout(hbox_total)
        self.setCentralWidget(central)
        self.setWindowTitle('Gomoku')
        
    """
    property
    * player
    """
    def setPlayer(self, player: Player, color: Color) -> None:
        if player.isAI():
            player.setStrategy(AIStrategy(color, self.search_view.updateSearch))
            player.strategy().Started.connect(lambda: self.search_view.clear())
            player.strategy().Finished.connect(self.finishDecision)
        else:
            player.setStrategy(PlayerStrategy(color, self.board_view.SquareDoubleClicked))
            player.strategy().Finished.connect(self.finishDecision)
        self.player_model[color] = player
        self.player_view[color].draw(player)
    
    """
    method
    * start, end
    * draw, drawSquare
    * placeStone
    """
    def start(self) -> None:
        self.draw()
        self.timer_count = self.player_model[Color.Black].timeLimit()
        self.timer.start(1000)

        self.player_view[self.current_turn].highlight()
        player_model = self.player_model[self.current_turn]
        player_model.strategy().start(self.board_model, player_model.timeLimit())

    def end(self, winner: Square) -> None:
        self.board_view.blockSignals(True)    ##########
        if winner is not None:
            player = self.player_model[winner]
            winner_string = f'승자는 <{winner.name}> {player.name()} 입니다.'
        else:
            winner_string = '무승부입니다.'
        QMessageBox.information(self, '결과', winner_string)

    def draw(self) -> None:
        self.board_view.draw(self.board_model)
        self.notation_view.draw(self.notation_model)

    def drawSquare(self, pos: Bitboard.P) -> None:
        self.board_view.drawSquare(self.board_model, pos)
        self.notation_view.draw(self.notation_model)
    
    def placeStone(self, color: Color, pos: Bitboard.P) -> None:
        self.timer.stop()
        self.board_model.setItem(pos, color)
        self.notation_model.addNote(BoardView.pos2note(pos))
        # self.undo_button.setEnabled(True)
        self.drawSquare(pos)
        winner = Rule.checkWin(self.board_model)
        if winner is not None:
            self.end(winner)
            return
        elif self.board_model.isFull():
            self.end(None)
            return

        before, next = self.current_turn, self.current_turn.opponent()
        self.player_view[before].setCount(self.player_model[before].timeLimit())
        self.current_turn = next
        self.timer_count = self.player_model[next].timeLimit()
        self.player_view[before].dehighlight()
        self.player_view[next].highlight()
        self.player_view[next].setCount(self.timer_count)
        self.timer.start(1000)
        player_model = self.player_model[self.current_turn]
        player_model.strategy().start(self.board_model, player_model.timeLimit())
    
    """
    slot
    * finishDecision
    * hideBoardOrder, showBoardOrder
    * squareSelected, squareEntered, squareLeaved
    * secondOut
    """
    @pyqtSlot()
    def finishDecision(self) -> None:
        player_model = self.player_model[self.current_turn]
        decision = player_model.strategy().choose()
        if self.board_model.item(decision) is not None:
            print('이미 돌이 있는 칸입니다.')
            player_model.strategy().restart(self.board_model)
            return
        if not Rule.isAble(self.board_model, self.current_turn, decision):
            print('금수입니다.')
            self.alert_view.alert('쌍삼')  # 금수
            player_model.strategy().restart(self.board_model)
            return
        self.placeStone(self.current_turn, decision)

    @pyqtSlot()
    def hideBoardOrder(self) -> None:
        self.board_view.is_show_order = False
        self.board_view.draw(self.board_model)

    @pyqtSlot()
    def showBoardOrder(self) -> None:
        self.board_view.is_show_order = True
        self.board_view.draw(self.board_model)

    @pyqtSlot(tuple)
    def squareEntered(self, pos: Bitboard.P) -> None:
        self.alert_view.alert(BoardView.pos2note(pos))

    @pyqtSlot(tuple)
    def squareLeaved(self, pos: Bitboard.P) -> None:
        self.alert_view.clear()
    
    @pyqtSlot()
    def secondOut(self) -> None:
        self.timer_count -= 1
        self.player_view[self.current_turn].setCount(self.timer_count)
        self.timer.setInterval(1000)
        if self.timer_count <= -5:  # 입력 지연 등의 처리를 위해 추가적으로 5초를 설정함
            self.timer.stop()
            self.end(self.current_turn.opponent())  # 시간 제한시 패배?
            return


    # Back Up function
    # @pyqtSlot()
    # def undo(self) -> None:
    #     note = self.notation_model.popNote()
    #     if note is not None:
    #         pos = BoardView.note2pos(note)
    #         self.board_model.setItem(pos, None)
    #         self.drawSquare(pos)
    #         # before turn이지만 일단 그냥 next turn으로 처리함. 턴 수를 화면에 표시하거나 한다면 문제가 생길수 있음
    #         self.nextTurn()
    #     self.undo_button.setEnabled(self.notation_model.peekNote() is not None)

    # def pause(self) -> None:
    #     remain = self.timer.remainingTime()
    #     self.timer.stop()
    #     QMessageBox.information(self, 'Pause', '일시정지')
    #     player_model = self.player_model[self.current_turn]
    #     player_model.strategy.search.stop()
    #     self.timer.start(remain)

    # def event(self, event: QEvent) -> bool:
    #     if isinstance(event, QKeyEvent) and event.key() == Qt.Key_Space:
    #         self.pause()
    #     return super().event(event)
