from mainProblem.rgbexpress import *


def parseDefaultEventDirDict(road: str) -> Dict[Dir, int]:
    dir_dict = {}
    if road in ['╵', '│', '┘', '└', '├', '┤', '┴', '┼']:
        dir_dict[Dir.Up] = 1
    if road in ['╷', '│', '┌', '┐', '├', '┤', '┬', '┼']:
        dir_dict[Dir.Down] = 1
    if road in ['╴', '─', '┐', '┘', '┤', '┬', '┴', '┼']:
        dir_dict[Dir.Left] = 1
    if road in ['╶', '─', '┌', '└', '├', '┬', '┴', '┼']:
        dir_dict[Dir.Right] = 1
    return dir_dict


def parseInitialState(data) -> RGBState:
    roads, trucks, items, cargos = data['Roads'], data['Trucks'], data['Items'], data['Cargos']

    map_list = roads.split('\n')
    ROW, COL = len(map_list), len(map_list[0])

    # create eventMap
    event_map: List[List[Optional[RGBEvent]]] = [[None for c in range(COL)] for r in range(ROW)]
    for truck in trucks:
        row, col = truck.pos
        dir_dict = parseDefaultEventDirDict(map_list[row][col])
        event_map[row][col] = RGBEvent(dir_dict, None, None)
    for color, pos_list in items.items():
        for row_iter, col_iter in pos_list:
            dir_dict = parseDefaultEventDirDict(map_list[row_iter][col_iter])
            event_map[row_iter][col_iter] = RGBEvent(dir_dict, color, None)
    for color, pos_list in cargos.items():
        for row_iter, col_iter in pos_list:
            dir_dict = parseDefaultEventDirDict(map_list[row_iter][col_iter])
            event_map[row_iter][col_iter] = RGBEvent(dir_dict, None, color)
    for row_iter in range(ROW):
        for col_iter in range(COL):
            if map_list[row_iter][col_iter] not in [' ', '│', '─'] and event_map[row_iter][col_iter] is None:
                dir_dict = parseDefaultEventDirDict(map_list[row_iter][col_iter])
                event_map[row_iter][col_iter] = RGBEvent(dir_dict, None, None)

    # update possible length
    for row_iter in range(ROW):
        for col_iter in range(COL):
            if event_map[row_iter][col_iter] is not None:
                for dir_iter in [Dir.Right, Dir.Down]:
                    if event_map[row_iter][col_iter].intersection.get(dir_iter) is not None:
                        count = 1
                        next_row, next_col = nextPos((row_iter, col_iter), dir_iter, count)
                        while event_map[next_row][next_col] is None:
                            count += 1
                            next_row, next_col = nextPos((row_iter, col_iter), dir_iter, count)
                        event_map[row_iter][col_iter].intersection[dir_iter] = count
                        event_map[next_row][next_col].intersection[dir_iter.opponent()] = count

    # print parsing result
    # for row_iter in range(ROW):
    #     for col_iter in range(COL):
    #         e = event_map[row_iter][col_iter]
    #         if e is not None:
    #             print((row_iter, col_iter), ' <Item:', e.item, '> <Cargo:', e.cargo, '> ', e.intersection)
    return RGBState(trucks, event_map)
