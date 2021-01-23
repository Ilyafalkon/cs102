import argparse
import pathlib




def read_map(path: str):
    path = pathlib.Path(path)
    with path.open() as f:
        map = f.read()
    return map

def create_list_with_numbers(map: str):
    grid = []
    newline = ""
    for symbol in map:
        if symbol == "☒":
            newline += "0"
        elif symbol == "☺":
            newline += "1"
        elif symbol == ".":
            newline += "."
        elif symbol == "☼":
            newline += "5"
        else:
            grid.append(newline)    
            newline = ""   
    return grid


def find_position(grid: list):
    for row in grid:
        for symbol in row:
            if symbol == 1:
                return (row, row.index(symbol))


def solve(grid: list):
    solved = False
    while not solved:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('map')
    args = parser.parse_args()
    map = read_map(args.map)
    grid = create_list_with_numbers(map)
    print(grid)