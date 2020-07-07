from problem import *
from typing import Tuple, Dict
import itertools


MAX_ITEM_COUNT = 3  # 한 트럭에 실을 수 있는 화물 최대 개수


# 트럭이 정지할 수 있기 때문에 Stop을 포함한다.
class Dir(Enum):
    Up = (-1, 0)
    Down = (1, 0)
    Left = (0, -1)
    Right = (0, 1)
    Stop = (0, 0)

    def opponent(self) -> 'Dir':
        if self == Dir.Left:
            return Dir.Right
        elif self == Dir.Right:
            return Dir.Left
        elif self == Dir.Up:
            return Dir.Down
        elif self == Dir.Down:
            return Dir.Up
        return Dir.Stop


Pos = Tuple[int, int]


# pos에서 dir 방향으로 count만큼 움직인 후의 좌표를 반환한다.
def nextPos(pos: Pos, dir: Dir, count: int):
    new_x, new_y = pos
    dir_x, dir_y = dir.value
    return new_x + dir_x * count, new_y + dir_y * count


class Color(Enum):
    Red = "r"
    Green = "g"
    Blue = "b"
    Yellow = 'y'


class Truck:
    def __init__(self, index: int, color: Color, dir: Dir, pos: Pos):
        self.index = index      # truck의 인덱스
        self.color = color
        self.dir = dir          # truck이 바라보고 있는 또는 움직이고 있는 방향
        self.pos = pos          # truck의 현재 위치
        self.remain = 0         # truck이 다음 event까지 도달하기 위해 남은 거리
        self.item_count = 0     # 싣고 있는 화물의 개수

    # t만큼 목적지를 향해 움직인다.
    def setProgress(self, t: int) -> None:
        self.pos = nextPos(self.pos, self.dir, t)
        self.remain -= t

    def copy(self) -> 'Truck':
        new_truck = Truck(self.index, self.color, self.dir, self.pos)
        new_truck.remain = self.remain
        new_truck.item_count = self.item_count
        return new_truck


# 교차점, 화물, 창고 이벤트를 관리하는 객체
class RGBEvent:
    def __init__(self, inter: Dict[Dir, int], item: Optional[Color] = None, cargo: Optional[Color] = None):
        """
        intersection은 교차로 정보를 담고 있는 Dictionary이다.
        key는 열려있는 교차로의 방향이고,
        value는 해당 방향으로 움직일 때 다음 event까지 도달하기 위한 거리를 의미한다.
        """
        self.intersection = {dir: count for dir, count in inter.items()}
        self.item = item        # 화물이 해당 event 구역에 없다면 None
        self.cargo = cargo      # 창고가 해당 event 구역에 없다면 None

    # 해당 dir의 교차로 정보를 없애, 더 이상 해당 방향으로 들어오거나 나갈 수 없게 한다.
    def removeDir(self, dir: Dir) -> None:
        del self.intersection[dir]

    def hasItem(self) -> bool:
        return self.item is not None

    def isCargo(self) -> bool:
        return self.cargo is not None

    def copy(self) -> 'RGBEvent':
        return RGBEvent(self.intersection, self.item, self.cargo)


# RGB Problem의 State는 트럭의 상태 리스트와 event를 담는 이중 리스트(지도)로 표현된다.
class RGBState(State):
    def __init__(self, trucks: List[Truck], eventMap: List[List[RGBEvent]]):
        super().__init__()
        self.trucks = [t.copy() for t in trucks]
        self.eventMap = [[e if e is None else e.copy() for e in list_iter] for list_iter in eventMap]

    def event(self, pos: Pos) -> Optional[RGBEvent]:
        return self.eventMap[pos[0]][pos[1]]

    def copy(self) -> 'RGBState':
        return RGBState(self.trucks, self.eventMap)


# RGB Problem에서 한 Action은 트럭의 index와 움직여야 하는 방향, 움직일 거리로 표현된다.
class RGBAction(Action):
    def __init__(self, moves: List[Tuple[int, Dir, int]]):  # index, dir, count
        self.__moves = moves

    def value(self) -> List[Tuple[int, Dir, int]]:
        return self.__moves


def rgbActions(state: RGBState) -> List[RGBAction]:
    """
    action_list: 최종 반환될 RGBAction 리스트
    each_truck_move_dict: 각각의 트럭별로 가능한 move들의 tuple들을 리스트로 저장해 둔 Dictionary
    pos_list: 충돌 테스트를 위해서 현재 트럭들의 위치를 차례대로 저장
    NO_ACTION: 규칙에 위배되거나 더 이상 움직일 곳이 없다면 NO_ACTION을 반환
    """
    action_list: List[RGBAction] = []
    each_truck_move_dict: Dict[int, List[Tuple[int, Dir, int]]] = {}
    pos_list: List[Pos] = []
    NO_ACTION = []

    # 트럭별로 가능한 move들을 탐색하여 each_truck_action_dict에 저장함
    # 충돌, 화물, 창고, 교차로 테스트를 진행
    for truck in state.trucks:
        pos = truck.pos
        event = state.event(pos)

        # crash test (현재위치에서 다른 트럭이랑 충돌하는지 확인)
        if pos in pos_list:
            return NO_ACTION
        pos_list.append(pos)

        if event is None or truck.dir == Dir.Stop:
            pass
        else:
            each_truck_move_dict[truck.index] = []
            # cargo test: 창고에서 화물을 내릴 수 없다면 NO_ACTION 반환
            if event.isCargo():
                if truck.color == event.cargo and truck.item_count > 0:
                    # 만일 화물을 내리는 데에 성공한다면, 여기에서 더 이상 움직이지 않고 멈출 수도 있음
                    each_truck_move_dict[truck.index].append((truck.index, Dir.Stop, 0))
                else:
                    return NO_ACTION
            # item test: 화물칸에서 화물을 실을 수 없다면 NO_ACTION 반환
            if event.hasItem():
                if not (truck.color == event.item and truck.item_count < MAX_ITEM_COUNT):
                    return NO_ACTION
            # intersection test: 교차로 정보를 참조하여 가능한 Dir로 move 추가
            for (dir_iter, dir_value) in event.intersection.items():
                # crash test (동일한 길로 다른 트럭이 동시진입하는지 확인)
                next_pos = nextPos(pos, dir_iter, dir_value)
                if next_pos in pos_list:
                    next_truck_index = pos_list.index(next_pos)
                    if each_truck_move_dict.get(next_truck_index):
                        will_crash = 0 < len(list(filter(lambda move: move[1] == dir_iter.opponent(),
                                                         each_truck_move_dict[next_truck_index])))
                        if will_crash:
                            continue
                each_truck_move_dict[truck.index].append((truck.index, dir_iter, dir_value))

    # each_truck_move_dict에서 트럭 index를 기준으로 cartesian product 계산
    total_truck_move_list: List[List[Tuple[int, Dir, int]]] = list(map(list, itertools.product(*[truck_dirs for truck_dirs in each_truck_move_dict.values()])))

    # 움직여야 하는 트럭이 없거나( [[]] ), 움직여야 하는데 움직일 수 없다면( [] ) NO_ACTION 반환
    if total_truck_move_list == [[]] or total_truck_move_list == []:
        return NO_ACTION

    for move_iter in total_truck_move_list:
        action_list.append(RGBAction(move_iter))
    return action_list


def rgbTrans(state: RGBState, action: RGBAction) -> RGBState:
    new_state = state.copy()

    # 출발 전에 출발지에서 화물을 싣고 내릴 수 있다면 수행하기
    for truck in new_state.trucks:
        event = new_state.event(truck.pos)
        if event is not None:
            if event.isCargo():
                truck.item_count -= 1
                event.cargo = None
            if event.hasItem():
                truck.item_count += 1
                event.item = None
    
    # action을 참조하여 트럭들의 다음 방향과 시간 설정하기
    for index, dir, count in action.value():
        truck = new_state.trucks[index]
        truck.dir = dir
        truck.remain = count
        # 출발한 교차로의 dir과, 반대쪽 교차로의 dir을 지움
        if dir != Dir.Stop:
            # dir 삭제
            new_state.event(truck.pos).removeDir(dir)
            new_state.event(nextPos(truck.pos, dir, count)).removeDir(dir.opponent())

    # 트럭들의 remain중 최솟값을 저장하기
    min_remain = None
    for truck in new_state.trucks:
        if truck.dir != Dir.Stop:
            if min_remain is None or min_remain > truck.remain:
                min_remain = truck.remain
    if min_remain is None:  # 움직여야하는 트럭이 없다면 더 이상 움직이지 않음
        min_remain = 0

    # min_remain만큼 트럭들을 움직이기
    for truck in new_state.trucks:
        truck.setProgress(min_remain)

    return new_state


# 모든 창고 이벤트를 완료하였는지 확인
def rgbGoalTest(state: RGBState) -> bool:
    result = True
    for truck in state.trucks:
        result = result and truck.dir == Dir.Stop
    if result is False:
        return result
    for list_iter in state.eventMap:
        for event in list_iter:
            result = result and (event is None or event.cargo is None)
    return result


# RGB Action의 비용은 정지하지 않은 트럭들의 remain의 최솟값이다.
def rgbActionCost(state: RGBState, action: RGBAction) -> int:
    min_remain = None
    dir_list = [truck.dir for truck in state.trucks]
    remain_list = [truck.remain for truck in state.trucks]
    
    # 주어진 action에 의해 변하는 remain을 remain_list에 반영
    for index, dir, count in action.value():
        dir_list[index] = dir
        remain_list[index] = count

    # 원래 정지해있지 않은 트럭들의 remain의 최솟값을 저장
    for index in range(len(state.trucks)):
        if dir_list[index] != Dir.Stop:
            if min_remain is None or min_remain > remain_list[index]:
                min_remain = remain_list[index]

    if min_remain is None:
        return 0
    else:
        return min_remain


def createRGBExpressProblem(initial_state: RGBState) -> Problem:
    return Problem(initial_state, rgbActions, rgbTrans, rgbGoalTest, rgbActionCost
)

