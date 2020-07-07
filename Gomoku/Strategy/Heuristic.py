from typing import List
from Model.LineQuery import *
from Model.GameBoard import *
from Model.Rule import *
import time


"""
Heuristic
보드의 상태를 받아 Heuristic Evaluation Value를 제공하는 클래스이다.
"""
class Heuristic:
    # 싱글턴 패턴
    _INSTANCE = None
    @classmethod
    def _getInstance(cls) -> 'Heuristic':
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def __init__(self):
        self.__parsed_eval_dict: Dict[LineQuery, Tuple[int, int]] = {}
        self.__pattern5: List[LineQuery] = []
        self.__pattern_closed4: List[LineQuery] = []
        self.__pattern_open3: List[LineQuery] = []

        for re_iter, value_tuple_iter in Heuristic._EvaluationDict.items():
            parsed_list = self.__parsePattern(re_iter)
            for parsed_ptn_iter in parsed_list:
                query_iter = LineQuery(parsed_ptn_iter)
                self.__parsed_eval_dict[query_iter] = value_tuple_iter
                if value_tuple_iter[0] >= Heuristic.Rank_5:
                    self.__pattern5.append(query_iter)
                elif value_tuple_iter[0] == Heuristic.Rank_Closed4:
                    self.__pattern_closed4.append(query_iter)
                elif value_tuple_iter[0] == Heuristic.Rank_Open3:
                    self.__pattern_open3.append(query_iter)

    """
    property
    * queryDict
    * patternList3, patternList4, patternList5
    """
    @classmethod
    def getQueryDict(cls) -> Dict[LineQuery, Tuple[int, int]]:
        return cls._getInstance().__parsed_eval_dict

    @classmethod
    def patternListOpen3(cls) -> List[LineQuery]:
        return cls._getInstance().__pattern_open3

    @classmethod
    def patternListClosed4(cls) -> List[LineQuery]:
        return cls._getInstance().__pattern_closed4

    @classmethod
    def patternList5(cls) -> List[LineQuery]:
        return cls._getInstance().__pattern5

    """
    Evaluation_regular_expression
    O: 내 돌
    X: 상대 돌
    _: 빈칸
    o: 내 돌이 아닌것
    x: 상대 돌이 아닌것
    b: 좌우 비대칭
    """
    # Line Priority Value
    Win = 100000
    Lose = -100000
    Rank_5 = 100000
    Rank_Open4 = 99999
    Rank_Closed4 = 95000
    Rank_Open3 = 20000

    Threat_Value = -Rank_Open3 + 2000

    # MultiLine Value
    EvalM_44 = (99999, 95000)  # 44, 열린4와 같음
    EvalM_43 = (99000, 94000)  # 43, 44보다 약간 낮음
    EvalM_33 = (-10000000, 10000000)  # 33, 금수

    _EvaluationDict = {
        # 4개 이상
        'oOOOOOo': (100000, 100000),    # 오목
        '__OOOO__': (99999, 95000),     # 열린4
        'b__OOOO_X': (99999, 95000),    # 열린4
        'b_O_OOO_': (95000, 2000),      # 닫힌4
        'bXOOOO_o': (95000, 2000),      # 닫힌4
        'bXO_OOOX': (95000, 2000),      # 닫힌4
        'bXOOO_Oo': (95000, 2000),      # 닫힌4
        'oOO_OOo': (95000, 2000),       # 닫힌4
        # 3개
        '__OOO__': (20000, 1500),       # 열린3, 완전개방
        'bX_OOO__': (20000, 1400),      # 열린3, 일부개방
        'bo_OO_O_o': (20000, 1400),     # 열린3, 띈3
        'bXO_OO_o': (3000, 600),        # 닫힌3, 띈3
        'oO_O_Oo': (2000, 400),         # 닫힌3
        'bXOO_O_o': (1500, 300),        # 닫힌3
        'bXOOO__o': (1500, 300),        # 닫힌3
        'X_OOO_X': (1500, 300),         # 닫힌3
        # 2개
        '__OO__': (1500, 300),          # 열린2, 완전개방
        '__O_O__': (1500, 300),         # 열린2, 완전개방
        'bX_OO__o': (1000, 200),        # 열린2, 일부개방
        'o_O__O_o': (500, 100),         # 열린2, 띈3만 연결가능
        'bXOO___o': (200, 40),          # 닫힌2
    }

    # Mapping evaluation expression to list of pattern
    def __parsePattern(self, re: str) -> List[str]:
        queue = [re] if re[0] != 'b' else [re[1:], re[1:][::-1]]
        result = []
        while queue:
            current_re = queue.pop(0)
            # parse o(not O) and x(not X)
            if current_re.find('o') != -1:
                queue.append(current_re.replace('o', '_', 1))
                queue.append(current_re.replace('o', 'X', 1))
            elif current_re.find('x') != -1:
                queue.append(current_re.replace('x', '_', 1))
                queue.append(current_re.replace('x', 'O', 1))
            else:
                result.append(current_re)
        return result

    """
    method
    * evaluation
    """
    EvalCount = 0
    EvalTotalTime = 0
    @classmethod
    def evaluation(cls, state: GameBoard, current_color: Color) -> int:
        start_time = time.time()
        Heuristic.EvalCount += 1

        # query를 보드에서 탐색한 개수만큼 가중치를 두어 계산함. 자신의 값에서 상대방의 값을 뺌
        current_closed4, current_open3 = [], []
        incurrent_closed4, incurrent_open3 = [], []
        line_value = 0
        for query_iter, (atk_value_iter, dfd_value_iter) in cls.getQueryDict().items():
            if query_iter in cls.patternList5():
                current_count = state.lineQueryCount(current_color, query_iter)
                incurrent_count = state.lineQueryCount(current_color.opponent(), query_iter)
                if current_count > 0:
                    return Heuristic.Win
                if incurrent_count > 0:
                    return Heuristic.Lose
            elif query_iter in cls.patternListClosed4():
                for current_result, current_pattern in state.lineQueryResultWithPattern(current_color, query_iter).values():
                    if current_result.count() != 0:
                        line_value += current_result.count() * atk_value_iter
                        current_closed4.append(current_pattern)
                for incurrent_result, incurrent_pattern in state.lineQueryResultWithPattern(current_color.opponent(), query_iter).values():
                    if incurrent_result.count() != 0:
                        line_value -= incurrent_result.count() * dfd_value_iter
                        incurrent_closed4.append(incurrent_pattern)
            elif query_iter in cls.patternListOpen3():
                for current_result, current_pattern in state.lineQueryResultWithPattern(current_color, query_iter).values():
                    if current_result.count() != 0:
                        line_value += current_result.count() * atk_value_iter
                        current_open3.append(current_pattern)
                for incurrent_result, incurrent_pattern in state.lineQueryResultWithPattern(current_color.opponent(), query_iter).values():
                    if incurrent_result.count() != 0:
                        line_value -= incurrent_result.count() * dfd_value_iter
                        incurrent_open3.append(incurrent_pattern)
            else:
                current_count = state.lineQueryCount(current_color, query_iter)
                incurrent_count = state.lineQueryCount(current_color.opponent(), query_iter)
                line_value += atk_value_iter * current_count - dfd_value_iter * incurrent_count

        # multi line check (44, 43, 33)
        # 33
        last_action_mask = Bitboard.pos2mask(state.lastAction())
        current_open3_count = len(current_open3)
        for i in range(current_open3_count - 1):
            for j in range(i + 1, current_open3_count):
                if current_open3[i] & current_open3[j] & last_action_mask:
                    return Heuristic.EvalM_33[0]
        incurrent_open3_count = len(incurrent_open3)
        for i in range(incurrent_open3_count - 1):
            for j in range(i + 1, incurrent_open3_count):
                if incurrent_open3[i] & incurrent_open3[j] & last_action_mask:
                    return Heuristic.EvalM_33[1]
        # 44
        current_closed4_count = len(current_closed4)
        for i in range(current_closed4_count - 1):
            for j in range(i, current_closed4_count):
                if current_closed4[i] & current_closed4[j]:
                    # 원래의 중복된 닫힌 4 공격값은 제거해준다.
                    line_value += Heuristic.EvalM_44[0] - Heuristic.Rank_Closed4 * 2
        incurrent_closed4_count = len(incurrent_closed4)
        for i in range(incurrent_closed4_count - 1):
            for j in range(i, incurrent_closed4_count):
                if incurrent_closed4[i] & incurrent_closed4[j]:
                    # 원래의 중복된 닫힌 4 방어값은 제거해준다.
                    line_value -= Heuristic.EvalM_44[1] - 2000 * 2
        # 43
        for closed4_iter in current_closed4:
            for open3_iter in current_open3:
                if closed4_iter & open3_iter:
                    # 원래의 중복된 닫힌 4, 열린 3 공격값은 제거해준다.
                    line_value += Heuristic.EvalM_43[0] - Heuristic.Rank_Closed4 - Heuristic.Rank_Open3
        for closed4_iter in incurrent_closed4:
            for open3_iter in incurrent_open3:
                if closed4_iter & open3_iter:
                    # 원래의 중복된 닫힌 4, 열린 3 방어값은 제거해준다.
                    line_value -= Heuristic.EvalM_43[1] - 3500

        end_time = time.time()
        Heuristic.EvalTotalTime += end_time - start_time
        if line_value >= Heuristic.Win:
            line_value = Heuristic.Win - 1
        elif line_value <= Heuristic.Lose:
            line_value = Heuristic.Lose + 1
        return line_value

    """
    debug method
    * printDefaultEvaluation
    """
    def printDefaultEvaluation(self) -> None:
        for re_iter, value_tuple_iter in Heuristic._EvaluationDict.items():
            print(f'{re_iter:<8}  {value_tuple_iter}')

Heuristic._getInstance()
