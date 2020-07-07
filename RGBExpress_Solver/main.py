from search import *
from data import Data
import time


def solve(code: str, show_log: bool = False, print_func = print):
    print(f'##### {code} Problem #####')
    print()

    start_time = time.time()
    result = uniform_search(Data.problem(code), show_log=show_log)
    exec_time = time.time() - start_time

    print(f'Uniform Search Result: {exec_time}')
    print_func(result)
    print()

    start_time = time.time()
    result = iterative_lengthening_search(Data.problem(code), show_log=show_log)
    exec_time = time.time() - start_time

    print(f'Iterative Lengthening Search Result: {exec_time}')
    print_func(result)
    print()

    print('############## End ##############')
    print()


def printBoard(actions) -> None:
    for row_iter in range(8):
        line = 'xxxxxxxx'
        y = actions[row_iter] - 1
        line = line[0:y] + 'Q' + line[(y+1):]
        print(line)


def printRGB(actions) -> None:
    if actions is None:
        print('No Solution')
        return

    from mainProblem.rgbexpress import Dir
    def arrow(dir: Dir) -> str:
        if dir == Dir.Stop:
            return '*'
        elif dir == Dir.Up:
            return '↑'
        elif dir == Dir.Down:
            return '↓'
        elif dir == Dir.Left:
            return '←'
        else:
            return '→'

    truck_dict = {}
    for action_iter in actions:
        for one_action in action_iter:
            index, dir, count = one_action
            if truck_dict.get(index) is None:
                truck_dict[index] = f"[Truck {index}] "
            truck_dict[index] += arrow(dir) + '.' * (max(count - 1, 0))

    for truck_string in truck_dict.values():
        print(truck_string)


# exec problem solving
show_log = True

# solve('Route-Finding', show_log=show_log)
# print()
# solve('8-Queens', show_log=show_log, print_func=printBoard)
# print()

"""
    Main Test Problem: RGB-Express
"""
# Custom / A-4 / A-9 / B-10 / C-2 / G-8 / P-7
# rgb_testcase = 'Custom'  # UCS: 0.004, ILS: 0.004
# rgb_testcase = 'A-4'    # UCS: 0.010, ILS: 0.033
rgb_testcase = 'A-9'    # UCS: 1.452, ILS: 1.534
# rgb_testcase = 'B-10'   # UCS: 0.028, ILS: 0.102
# rgb_testcase = 'C-2'    # UCS: 18.610, ILS: 5.367
# rgb_testcase = 'G-8'    # UCS: 0.559, ILS: 1.726
# rgb_testcase = 'P-7'    # UCS: 567.446, ILS: 45.627
solve(f'RGB-Express {rgb_testcase}', show_log=show_log, print_func=printRGB)
print()
