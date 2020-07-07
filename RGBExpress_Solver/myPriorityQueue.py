import heapq
from typing import Optional, Tuple


class MyPriorityQueue:
    def __init__(self):
        self.__queue = []

    def size(self) -> int:
        return len(self.__queue)

    def empty(self) -> bool:
        return self.size() == 0

    def put(self, item: Tuple) -> None:
        heapq.heappush(self.__queue, item)

    def get(self) -> Tuple:
        return heapq.heappop(self.__queue)

    def findItem(self, func) -> Optional[Tuple]:
        for item in self.__queue:
            if func(item):
                return item
        return None

    def remove(self, item: Tuple) -> None:
        self.__queue.remove(item)
        heapq.heapify(self.__queue)