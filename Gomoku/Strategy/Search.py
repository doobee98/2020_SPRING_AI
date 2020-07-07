from PyQt5.QtCore import *
from Strategy.Heuristic import *
from typing import Tuple, Optional
import random, time


"""
Search(QThread)
Alpha - Beat Pruning / Iterative Deepening을 이용해서 의사결정을 한다.
start 함수를 호출하면 run 메소드가 작동되며, stop 이후 terminate로 쓰레드를 강제종료 할 수 있다.
"""
class Search(QThread):
    UpdateNew = pyqtSignal(int, tuple, int)
    Finished = pyqtSignal()
    EVAL_MIN = -10000000
    EVAL_MAX = 10000000
    MAX_DEPTH = 5

    def __init__(self, board: GameBoard, color: Color):
        super().__init__()
        self.decision: Tuple[Optional[int], Optional[int]] = (None, None)
        self.board = board
        self.color = color
        self.start_time = 0

    """
    method
    * run
    * stop
    * openingTableSearch
    * alpha_beta_search
    * max_search, min_search
    * cutoffTest
    * createActions
    """
    # AI Decision
    def run(self) -> None:
        self.start_time = time.time()
        # 만약 첫 무브라면 테이블 참조 (테이블 만들기)
        opening_search_result = self.openingTableSearch()
        if opening_search_result is not None:
            self.decision = opening_search_result
        else:
            self.alpha_beta_search(self.board)
        self.stop()
        return

    def stop(self) -> None:
        print('decision: ', self.decision)
        if Heuristic.EvalCount > 0:
            Heuristic.EvalTotalTime = time.time() - self.start_time
            print(f'Evaluation: {Heuristic.EvalTotalTime / Heuristic.EvalCount:.10f} '
                  f'// {Heuristic.EvalCount, Heuristic.EvalTotalTime}\n')
            Heuristic.EvalCount = 0
            Heuristic.EvalTotalTime = 0
        self.Finished.emit()

    # 세번째 수 까지는 대부분 의미없는 탐색이기도 하고, 게임마다 변화를 주기 위해 랜덤 테이블을 사용함
    def openingTableSearch(self) -> Optional[Bitboard.P]:
        stone_count = self.board.count()
        if stone_count <= 2:
            if stone_count == 0:
                return Bitboard.Size // 2, Bitboard.Size // 2
            one_pos_table = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            two_pos_table = [(2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (-1, 2), (-2, 2), (-2, 1),
                             (-2, 0), (-2, -1), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (2, -1)]
            if stone_count == 1:
                pos_row, pos_col = one_pos_table[random.randrange(len(one_pos_table))]
                last_row, last_col = self.board.lastAction()
                if 1 <= last_row < Bitboard.Size - 1 and 1 <= last_col < Bitboard.Size - 1:
                    return last_row + pos_row, last_col + pos_col
                else:
                    return Bitboard.Size // 2, Bitboard.Size // 2
            else:  # stone_count == 2:  // 세 번째 수를 둔다: 첫 수를 AI가 뒀다: 첫 수가 9, 9다
                white_row, white_col = self.board.lastAction()
                black_row, black_col = Bitboard.Size // 2, Bitboard.Size // 2
                if (black_row - white_row, black_col - white_col) in one_pos_table:
                    # 두 돌이 붙어있다면 랜덤 table
                    white_diff = (black_row - white_row, black_col - white_col)
                    one_two_pos_table = one_pos_table + two_pos_table
                    one_two_pos_table.remove(white_diff)
                    pos_row, pos_col = one_two_pos_table[random.randrange(0, len(one_two_pos_table))]
                    return black_row + pos_row, black_col + pos_col
        return None

    # Alpha Beta Pruning
    # 검색 결과를 self.decision에 바로 반영하기 때문에 반환값이 없음 (쓰레드 강제종료시 값을 남기기 위함)
    def alpha_beta_search(self, board: GameBoard) -> None:
        initial_state = board
        max_value = Search.EVAL_MIN

        # max_value를 만드는 best_action 탐색, iterative deepning
        actions = Search.createActions(initial_state, 2)  # initial state는 coverage limit을 2로 둠
        reorder_action_list: List[Bitboard.P] = []  # depth가 낮을때의 탐색으로 좋았던 next move를 reordering함
        remove_action_list: List[Bitboard.P] = []  # 위협이 큰 노드는 더 이상 탐색하지 않음
        for depth_iter in range(1, Search.MAX_DEPTH + 1):
            for next_action_iter in actions:
                next_state = initial_state.copySelf()
                next_state.setItem(next_action_iter, self.color)
                next_search_value = self.min_search(next_state, max_value, Search.EVAL_MAX, depth_iter - 1)
                print(next_action_iter, next_search_value)
                if max_value < next_search_value:
                    self.decision = next_action_iter  # 바로바로 self.decision에 반영 (쓰레드가 언제 종료될지 모르니)
                    max_value = next_search_value
                    reorder_action_list.append(next_action_iter)
                    self.UpdateNew.emit(depth_iter, next_action_iter, max_value)
                    if max_value >= Heuristic.Win:
                        return
                # 크게 위협이 되는 Threat_Value보다 값이 낮을 경우 해당 행동은 더 이상 탐색하지 않음
                elif next_search_value <= Heuristic.Threat_Value:
                    remove_action_list.append(next_action_iter)
                # 현재 max_value와 같은 값이 나오면 그 값으로 업데이트하지는 않지만, reorder 리스트에는 넣어둠
                elif max_value == next_search_value:
                    reorder_action_list.insert(-1, next_action_iter)
            for reorder_action in reorder_action_list:
                actions.remove(reorder_action)
                actions.insert(0, reorder_action)
            for remove_action in remove_action_list:
                actions.remove(remove_action)
                print('removed:', remove_action)
            reorder_action_list = []
            remove_action_list = []
            max_value = Search.EVAL_MIN
            if len(actions) <= 1:
                return
        self.decision = actions[0]
        return

    # max_search: 내 돌을 두면서 eval을 가장 높이는 action 찾기
    def max_search(self, state: GameBoard, alpha: int, beta: int, depth: int) -> int:
        if self.cutoffTest(state, depth):
            return Heuristic.evaluation(state, self.color)
        v = Search.EVAL_MIN

        actions = Search.createActions(state, 2)
        for next_action_iter in actions:
            next_state = state.copySelf()
            next_state.setItem(next_action_iter, self.color)
            next_search_value = self.min_search(next_state, v, Search.EVAL_MAX, depth - 1)
            if v < next_search_value:
                v = next_search_value
                if v >= Heuristic.Win:
                    break
            if v >= beta:
                break
            alpha = max(alpha, v)
        return v

    # min_search: 상대 돌을 두면서 eval을 가장 낮추는 action 찾기
    def min_search(self, state: GameBoard, alpha: int, beta: int, depth: int) -> int:
        if self.cutoffTest(state, depth):
            return -Heuristic.evaluation(state, self.color.opponent())
        v = Search.EVAL_MAX

        actions = Search.createActions(state, 2)
        for next_action_iter in actions:
            next_state = state.copySelf()
            next_state.setItem(next_action_iter, self.color.opponent())
            next_search_value = self.max_search(next_state, alpha, beta, depth - 1)
            if v > next_search_value:
                v = next_search_value
                if v <= Heuristic.Lose:
                    break
            if v <= alpha:
                break
            beta = min(beta, v)
        return v

    # depth 제한을 넘었거나 winner가 존재하면 리턴
    def cutoffTest(self, state: GameBoard, depth: int) -> bool:
        winner = Rule.checkWin(state)
        return winner is not None or depth <= 0

    # 현재 돌이 두어져 있는 곳들 주변의 legal actions를 리턴함 (coverage limit만큼)
    @classmethod
    def createActions(cls, state: GameBoard, coverage_limit: int) -> List[Bitboard.P]:
        total_board = state.totalBoard()
        coverage_board = total_board
        for i in range( coverage_limit):
            coverage_board = coverage_board.dilation(1)
        coverage = coverage_board & ~total_board
        actions: List[Bitboard.P] = []
        for row_iter in range(Bitboard.Size):
            for col_iter in range(Bitboard.Size):
                if coverage.hasItem((row_iter, col_iter)) is True:
                    actions.append((row_iter, col_iter))
        return actions
