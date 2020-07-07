from Strategy.ChooseStrategy import *
from Strategy.Search import *


"""
AIStrategy
AI의 의사결정 클래스.
Search Thread에 처리 과정을 위임하고 시간을 잰다.
"""
class AIStrategy(ChooseStrategy):
    def __init__(self, color: Color, update_slot):
        super().__init__(color)
        self.__search: Optional[Search] = None  # ai action 탐색
        self.__update_slot = update_slot  # search에서 새로운 best move를 update할 때 마다 view를 업데이트하기 위한 함수
        self.__found = False
        self.timer.timeout.connect(self.timeOutStop)

    """
    inherited method
    * isActive
    * start
    * stop
    """
    def isActive(self) -> bool:
        return self.timer.isActive()

    def start(self, board: GameBoard, second_limit: int) -> None:
        self.timer.start(int(second_limit * 1000) - 500)  # 0.5초를 여유시간으로 줌
        self.__found = False
        self.Started.emit()
        if self.__search is not None:
            self.__search.UpdateNew.disconnect(self.__update_slot)
            self.__search.Finished.disconnect(self.searchFinished)
            self.__search = None
        self.__search = Search(board, self.color)
        self.__search.UpdateNew.connect(self.__update_slot)
        self.__search.Finished.connect(self.searchFinished)
        self.__search.start()

    def restart(self, board: GameBoard) -> None:
        self.timer.start()
        self.__found = False
        self.Started.emit()
        if self.__search is not None:
            self.__search.UpdateNew.disconnect(self.__update_slot)
            self.__search.Finished.disconnect(self.searchFinished)
            self.__search = None
        self.__search = Search(board, self.color)
        self.__search.UpdateNew.connect(self.__update_slot)
        self.__search.Finished.connect(self.searchFinished)
        self.__search.start()

    def stop(self) -> None:
        self.timer.stop()

    """
    slot
    * searchFinished
    * timeOutStop
    """
    @pyqtSlot()
    def searchFinished(self) -> None:
        if not self.__found:  # 쓰레드에서 중복호출될 수 있으므로 플래그로 방지함 (시간 종료와 탐색 종료가 동시에 발생시)
            if self.isActive():
                self.stop()
            self.__found = True
            self.setDecision(self.__search.decision)
            self.Finished.emit()

    # 시간이 거의 다 되면 호출되어 검색을 중지하고 쓰레드를 강제종료한다.
    @pyqtSlot()
    def timeOutStop(self) -> None:
        self.__search.stop()
        self.__search.terminate()
