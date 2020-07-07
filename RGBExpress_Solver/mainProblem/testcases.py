from mainProblem.rgbexpress import *


rgb_testcases = {
    'Custom': {
        # road tokens: '╴', '╶', '╵', '╷', '─', '│', '┌', '┐', '┘', '└', '├', '┤', '┬', '┴', '┼'
                # 0123456
        'Roads': " ┌─┬─┐ \n"  # 0
                 " │ │ │ \n"  # 1
                 " ├─┼─┤ \n"  # 2
                 " │ │ │ \n"  # 3
                 "╶┴─┴─┴╴",   # 4
        'Trucks': [
            Truck(0, Color.Red, Dir.Right, (4, 0)),
            Truck(1, Color.Green, Dir.Left, (4, 6))
        ],
        'Items': {
            Color.Red: [(2, 3)],
            Color.Green: [(2, 5)],
        },
        'Cargos': {
            Color.Red: [(3, 3)],
            Color.Green: [(1, 5)],
        }
    },
    'A-4': {
        # road tokens: '╴', '╶', '╵', '╷', '─', '│', '┌', '┐', '┘', '└', '├', '┤', '┬', '┴', '┼'
        'Roads': " ┌──┬──┐ \n"  # 0
                 " │  │  │ \n"  # 1
                 " ├──┼──┤ \n"  # 2
                 " │  │  │ \n"  # 3
                 " ├──┼──┤ \n"  # 4
                 " │  │  │ \n"  # 5
                 " │  │  │ \n"  # 6
                 " │  │  │ \n"  # 7
                 "╶┴──┴──┴╴",   # 8
        'Trucks': [
            Truck(0, Color.Red, Dir.Right, (8, 0)),
            Truck(1, Color.Green, Dir.Left, (8, 8))
        ],
        'Items': {
            Color.Red: [(2, 4)],
            Color.Green: [(4, 4)],
        },
        'Cargos': {
            Color.Red: [(0, 2)],
            Color.Green: [(0, 6)],
        }
    },
    'A-9': {
        # road tokens: '╴', '╶', '╵', '╷', '─', '│', '┌', '┐', '┘', '└', '├', '┤', '┬', '┴', '┼'
        'Roads': "╷     ╷\n"  # 0
                 "├─┬─┬─┤\n"  # 1
                 "│ │ │ │\n"  # 2
                 "├─┤ ├─┤\n"  # 3
                 "│ ├─┤ │\n"  # 4
                 "├─┤ ├─┤\n"  # 5
                 "│ │ │ │\n"  # 6
                 "├─┴─┴─┤\n"  # 7
                 "╵     ╵",   # 8
        'Trucks': [
            Truck(0, Color.Red, Dir.Up, (8, 0)),
            Truck(1, Color.Yellow, Dir.Up, (8, 6))
        ],
        'Items': {
            Color.Red: [(3, 2), (5, 2)],
            Color.Yellow: [(5, 4)],
        },
        'Cargos': {
            Color.Red: [(0, 0), (1, 3)],
            Color.Yellow: [(0, 6)],
        }
    },
    'B-10': {
        # road tokens: '╴', '╶', '╵', '╷', '─', '│', '┌', '┐', '┘', '└', '├', '┤', '┬', '┴', '┼'
        'Roads': "╷ ╷   ╷ ╷\n"  # 0
                 "│ ├─┬─┤ │\n"  # 1
                 "│ │ │ │ │\n"  # 2
                 "│ ├─┼─┤ │\n"  # 3
                 "│ │ │ │ │\n"  # 4
                 "└─┼─┼─┼─┘\n"  # 5
                 "  │ │ │  \n"  # 6
                 "  └─┴─┘  ",   # 7
        'Trucks': [
            Truck(0, Color.Red, Dir.Down, (0, 0)),
            Truck(1, Color.Green, Dir.Down, (0, 8))
        ],
        'Items': {
            Color.Red: [(3, 3), (7, 4)],
            Color.Green: [(5, 4)],
        },
        'Cargos': {
            Color.Red: [(0, 6), (3, 5)],
            Color.Green: [(0, 2)],
        }
    },
    'C-2': {
        # road tokens: '╴', '╶', '╵', '╷', '─', '│', '┌', '┐', '┘', '└', '├', '┤', '┬', '┴', '┼'
                 #012345678
        'Roads': "  ┌─┬─┐  \n"  # 0
                 "  │ │ │  \n"  # 1
                 "┌─┼─┼─┼─┐\n"  # 2
                 "│ │ │ │ │\n"  # 3
                 "└─┼─┼─┼─┘\n"  # 4
                 "  │ │ │  \n"  # 5
                 "  └─┼─┘  \n"  # 6
                 "    ╵    ",  # 7
        'Trucks': [
            Truck(0, Color.Blue, Dir.Up, (7, 4))
        ],
        'Items': {
            Color.Blue: [(1, 4), (3, 4), (5, 2), (5, 4), (5, 6)]
        },
        'Cargos': {
            Color.Blue: [(0, 3), (0, 5), (2, 1), (2, 7), (6, 5)]
        }
    },
    'G-8': {
        # road tokens: '╴', '╶', '╵', '╷', '─', '│', '┌', '┐', '┘', '└', '├', '┤', '┬', '┴', '┼'
        'Roads': "╶┬─┬─┬─┬─┬╴\n"  # 0
                 " │ │ │ │ │ \n"  # 1
                 " ├─┼─┼─┼─┤ \n"  # 2
                 " │ │ │ │ │ \n"  # 3
                 " ├─┼─┼─┼─┤ \n"  # 4
                 " │ │ │ │ │ \n"  # 5
                 " ├─┴─┼─┴─┤ \n"  # 6
                 " │   │   │ \n"  # 7
                 " ╵   ╵   ╵ ",  # 8
        'Trucks': [
            Truck(0, Color.Red, Dir.Up, (8, 1)),
            Truck(1, Color.Blue, Dir.Up, (8, 5)),
            Truck(2, Color.Green, Dir.Up, (8, 9)),
        ],
        'Items': {
            Color.Red: [(4, 1)],
            Color.Blue: [(2, 4), (4, 9)],
            Color.Green: [(3, 3)],
        },
        'Cargos': {
            Color.Red: [(0, 6)],
            Color.Blue: [(0, 2), (0, 8)],
            Color.Green: [(0, 4)],
        }
    },
    'P-7': {
        # road tokens: '╴', '╶', '╵', '╷', '─', '│', '┌', '┐', '┘', '└', '├', '┤', '┬', '┴', '┼'
        'Roads': "   ┌─┬─┐   \n"  # 0
                 " ┌─┼─┼─┼─┐ \n"  # 1
                 " │ │ │ │ │ \n"  # 2
                 "╶┼─┼─┼─┼─┼╴\n"  # 3
                 " │ │ │ │ │ \n"  # 4
                 "╶┼─┼─┼─┼─┼╴\n"  # 5
                 " │ │ │ │ │ \n"  # 6
                 " └─┴─┴─┴─┘ ",  # 7
        'Trucks': [
            Truck(0, Color.Red, Dir.Right, (3, 0)),
            Truck(1, Color.Yellow, Dir.Right, (5, 0)),
            Truck(2, Color.Yellow, Dir.Left, (3, 10)),
            Truck(3, Color.Red, Dir.Left, (5, 10)),
        ],
        'Items': {
            Color.Red: [(3, 1), (4, 9), (6, 7)],
            Color.Yellow: [(4, 1), (6, 1), (4, 3), (2, 5)],
        },
        'Cargos': {
            Color.Red: [(0, 6), (3, 8), (7, 8)],
            Color.Yellow: [(0, 4), (1, 2), (7, 2), (5, 4)],
        }
    },
}