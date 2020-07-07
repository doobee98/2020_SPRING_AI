from myPriorityQueue import *
from problem import *
from typing import Union


Node = Tuple[int, State, List[Action]]
getCost: Callable[[Node], int] = lambda node: node[0]
getState: Callable[[Node], State] = lambda node: node[1]
getPath: Callable[[Node], List[Action]] = lambda node: node[2]
getNode: Callable[[int, State, List[Action]], Node] = lambda cost, state, path: (cost, state, path)


def uniform_search(problem: Problem, show_log: bool = False) -> Optional[List[Action]]:
    frontier = MyPriorityQueue()
    explored = []
    cost_priority = 0   # show_log가 True일시, log를 출력하기 위해 현재 loop의 min cost를 저장한다.

    frontier.put(getNode(0, problem.initialState(), []))
    while not frontier.empty():
        current_node = frontier.get()
        current_cost, current_state, current_path = getCost(current_node), getState(current_node), getPath(current_node)
        if show_log and cost_priority < current_cost:
            cost_priority = current_cost
            print('\tPopped Cost:', cost_priority)
        if problem.isGoalState(current_state):
            print('< Optimal Cost', current_cost, '>')
            return current_path

        if current_state not in explored:
            explored.append(current_state)
        for action_iter in problem.actions(current_state):
            next_state = problem.doAction(current_state, action_iter)
            next_cost = current_cost + problem.pathCost(current_state, action_iter)
            next_path = current_path + [action_iter.value()]
            next_node = getNode(next_cost, next_state, next_path)
            searched_node = frontier.findItem(lambda node: getState(node) == next_state)
            if (next_state not in explored) and (searched_node is None):
                frontier.put(next_node)
            elif searched_node is not None:
                searched_cost, _, _ = searched_node
                if searched_cost > next_cost:
                    frontier.remove(searched_node)
                    frontier.put(next_node)
    return None


"""
    HomeWork Algorithm: Iterative Lengthening Search
"""
TypeSuccess = Tuple[int, List[Action]]  # Best Cost, Solution Path의 튜플
TypeFailure = type(None)
TypeCutoff = int                        # Cutoff된 Cost중 최솟값을 저장


def iterative_lengthening_search(problem: Problem, show_log: bool = False) -> Optional[List[Action]]:
    # recursive_CLS 함수는 주어진 cost limit에 대해 Success Tuple, Cutoff value, Failure 셋 중 하나를 반환한다.
    def recursive_CLS(state: State, cost: int, cost_limit: int) -> Union[TypeSuccess, TypeCutoff, TypeFailure]:
        if problem.isGoalState(state):
            return cost, []
        if cost > cost_limit:
            return cost

        cutoff_value = None     # Goal State나 Cutoff가 발생하지 않으면 그대로 Failure인 None이 되도록 초기값 설정
        for action_iter in problem.actions(state):
            next_state = problem.doAction(state, action_iter)
            next_cost = cost + problem.pathCost(state, action_iter)
            result = recursive_CLS(next_state, next_cost, cost_limit)
            # Cutoff시 Cutoff당한 cost중 최솟값을 cutoff_value에 저장한다.
            if isinstance(result, TypeCutoff):
                if cutoff_value is None or result < cutoff_value:
                    cutoff_value = result
            # Failure시 이 state는 무시하고 다음 state를 탐색함
            elif isinstance(result, TypeFailure):
                continue
            # 둘 다 아니라면 Solution Path를 더해줌
            else:
                cost, action_list = result
                return cost, [action_iter.value()] + action_list
        return cutoff_value

    cost_limit = 0
    while True:
        if show_log:
            print('\tFind Cost:', cost_limit)
        result = recursive_CLS(problem.initialState(), 0, cost_limit)
        # Cutoff될 시 다음 Cost Limit은 Cutoff된 최소의 Cost를 이용하여 재탐색 (cost_limit이 증가함)
        if isinstance(result, TypeCutoff):
            cost_limit = result
        # recursive_CLS의 결과가 None일시 가능한 Path가 없으므로 None 반환
        elif isinstance(result, TypeFailure):
            return None
        # 탐색에 성공했을 경우 최적 코스트를 출력 후 해당 액션 리스트를 반환함
        else:
            cost, action_list = result
            print('< Optimal Cost', cost, '>')
            return action_list
