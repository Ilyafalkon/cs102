import argparse
import pathlib
import typing


def read_map(path: pathlib.Path):
    path = pathlib.Path(path)
    with path.open() as f:
        map = f.read()
    return map + "\n"


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


def make_matrix(grid: list):
    matrix = []
    sub_matrix = []
    for line in grid:
        for symbol in line:
            sub_matrix.extend(symbol)
        matrix.append(sub_matrix)
        sub_matrix = []
    return matrix


def find_position(grid: list):
    for row in grid:
        for symbol in row:
            if symbol == "1":
                return (grid.index(row), row.index(symbol))


def find_destination(grid: list):
    for row in grid:
        for symbol in row:
            if symbol == "5":
                return (grid.index(row), row.index(symbol))


def solve(grid: list, curr_pos: typing.Tuple[int, int]):
    solved = False
    row2, col2 = find_destination(grid)
    row, col = curr_pos
    if (
        grid[row2 - 1][col2] == "1"
        or grid[row2 + 1][col2] == "1"
        or grid[row2][col2 - 1] == "1"
        or grid[row2][col2 + 1] == "1"
    ):
        return grid
    if (
        grid[row + 1][col] != "."
        and grid[row - 1][col] != "."
        and grid[row][col + 1] != "."
        and grid[row][col - 1] != "."
    ):
        return None
    while not solved:
        if (
            grid[row2 - 1][col2] == "1"
            or grid[row2 + 1][col2] == "1"
            or grid[row2][col2 - 1] == "1"
            or grid[row2][col2 + 1] == "1"
        ):
            solved = True
        if grid[row + 1][col] == ".":
            grid[row + 1][col] = "1"
            if solve(grid, (row + 1, col)):
                return solve(grid, (row + 1, col))
            else:
                grid[row + 1][col] = "3"
        elif grid[row - 1][col] == ".":
            grid[row - 1][col] = "1"
            if solve(grid, (row - 1, col)):
                return solve(grid, (row - 1, col))
            else:
                grid[row - 1][col] = "3"
        elif grid[row][col - 1] == ".":
            grid[row][col - 1] = "1"
            if solve(grid, (row, col - 1)):
                return solve(grid, (row, col - 1))
            else:
                grid[row][col - 1] = "3"
        elif grid[row][col + 1] == ".":
            grid[row][col + 1] = "1"
            if solve(grid, (row, col + 1)):
                return solve(grid, (row, col + 1))
            else:
                grid[row][col + 1] = "3"
    return grid


def print_map(matrix: list):
    line = ""
    for row in matrix:
        for symbol in row:
            if symbol == "0":
                line += "☒"
            if symbol == "." or symbol == "3":
                line += "."
            if symbol == "1":
                line += "☺"
            if symbol == "5":
                line += "☼"
        line += "\n"
    return line


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map")
    args = parser.parse_args()
    map = read_map(args.map)
    grid = create_list_with_numbers(map)
    matrix = make_matrix(grid)
    grid = solve(matrix, find_position(matrix))
    print(print_map(grid))
