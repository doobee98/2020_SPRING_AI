from problem import *
from typing import Tuple


class RouteInfo:
    Arad = 'Arad'
    Zerind = 'Zerind'
    Oradea = 'Oradea'
    Sibiu = 'Sibiu'
    Fagaras = 'Fagaras'
    Bucharest = 'Bucharest'
    Urziceni = 'Urziceni'
    Vaslui = 'Vaslui'
    Iasi = 'Iasi'
    Neamt = 'Neamt'
    Hirsova = 'Hirsova'
    Eforie = 'Eforie'
    Giurgiu = 'Giurgiu'
    Pitesti = 'Pitesti'
    RimnicuVilcea = 'Rimnicu Vilcea'
    Craiova = 'Craiova'
    Drobeta = 'Drobeta'
    Mehadia = 'Mehadia'
    Lugoj = 'Lugoj'
    Timisoara = 'Timisoara'


class RouteState(State):
    def __init__(self, name: str):
        super().__init__()
        self.__name = name

    def name(self) -> str:
        return self.__name


class RouteAction(Action):
    def __init__(self, go: str):
        self.__go = go

    def value(self) -> str:
        return self.__go


edge_db: List[Tuple[str, str, int]] = [
    (RouteInfo.Arad, RouteInfo.Zerind, 75),
    (RouteInfo.Arad, RouteInfo.Sibiu, 140),
    (RouteInfo.Arad, RouteInfo.Timisoara, 118),
    (RouteInfo.Zerind, RouteInfo.Oradea, 71),
    (RouteInfo.Oradea, RouteInfo.Sibiu, 151),
    (RouteInfo.Sibiu, RouteInfo.Fagaras, 99),
    (RouteInfo.Sibiu, RouteInfo.RimnicuVilcea, 80),
    (RouteInfo.Fagaras, RouteInfo.Bucharest, 211),
    (RouteInfo.Bucharest, RouteInfo.Urziceni, 85),
    (RouteInfo.Urziceni, RouteInfo.Vaslui, 142),
    (RouteInfo.Vaslui, RouteInfo.Iasi, 92),
    (RouteInfo.Iasi, RouteInfo.Neamt, 87),
    (RouteInfo.Urziceni, RouteInfo.Hirsova, 98),
    (RouteInfo.Hirsova, RouteInfo.Eforie, 86),
    (RouteInfo.Bucharest, RouteInfo.Giurgiu, 90),
    (RouteInfo.Bucharest, RouteInfo.Pitesti, 101),
    (RouteInfo.Pitesti, RouteInfo.RimnicuVilcea, 97),
    (RouteInfo.Craiova, RouteInfo.Pitesti, 138),
    (RouteInfo.Craiova, RouteInfo.RimnicuVilcea, 146),
    (RouteInfo.Craiova, RouteInfo.Drobeta, 120),
    (RouteInfo.Drobeta, RouteInfo.Mehadia, 75),
    (RouteInfo.Mehadia, RouteInfo.Lugoj, 70),
    (RouteInfo.Lugoj, RouteInfo.Timisoara, 111)
]

def routeActions(state: RouteState) -> List[Action]:
    action_list = []
    for city1, city2, cost in edge_db:
        if state.name() == city1:
            action_list.append(RouteAction(city2))
        elif state.name() == city2:
            action_list.append(RouteAction(city1))
    return action_list

def routeTrans(state: RouteState, action: RouteAction) -> RouteState:
    for city1, city2, cost in edge_db:
        if (state.name(), action.value()) == (city1, city2):
            return RouteState(city2)
        elif (state.name(), action.value()) == (city2, city1):
            return RouteState(city1)
    raise ValueError

def routeGoalTest(state: RouteState) -> bool:
    return state.name() == RouteInfo.Bucharest

def routeActionCost(state: RouteState, action: RouteAction) -> int:
    for city1, city2, cost in edge_db:
        if (state.name(), action.value()) == (city1, city2) or (state.name(), action.value()) == (city2, city1):
            return cost
    raise ValueError


routeProblem = Problem(
    RouteState(RouteInfo.Arad),         # initial state
    routeActions,                       # actions
    routeTrans,                         # transition model
    routeGoalTest,                      # goal test
    routeActionCost                     # action cost
)