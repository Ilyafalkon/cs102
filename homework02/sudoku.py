import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    list_Of_Elements = [ values[n*i-n:n*i] for i in range(1, len(values)//n + 1) ]
    return list_Of_Elements
    


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row_WeNeed = grid[pos[0]]
    return row_WeNeed 



def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """

    col_WeNeed = [grid[i][pos[1]] for i in range(len(grid[0]))]
    return col_WeNeed


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    Number_OfBlock = (pos[0]//3, pos[1]//3)
    row, col = Number_OfBlock
    row_InBlock = int(len(grid[0])**0.5)
    block_WeNeed = []
    for row in range(3*row, 3*row + row_InBlock):
        block_WeNeed.extend([grid[row][col] for col in range(col*3, col*3 + row_InBlock)])
    return block_WeNeed


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    position = ""
    for row in range(0, len(grid[0])):
        for num in range(0, len(grid[0])):
            if grid[row][num] == ".":
                position = (row, num)
                return position
    if position == "":
        return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    nums_InRow = {str(i) for i in range(1,10) if str(i) not in get_row(grid, pos)}
    nums_InCol = {str(i) for i in range(1,10) if str(i) not in get_col(grid, pos)}
    nums_InBlock = {str(i) for i in range (1,10) if str(i) not in get_block(grid,pos)}
    possible_values = nums_InBlock & nums_InRow & nums_InCol
    return possible_values



def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    if find_empty_positions(grid) == None:
        return grid
    else:
        position = find_empty_positions(grid)
        values = find_possible_values(grid, position)
        for num in values:
            if num not in "123456789":
                return False
        for num in values: 
            row, col = position
            grid[row][col] = str(num)
            if (solve(grid)):
                return grid
            else:
                grid[row][col] = "."
    return None
              


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    check = True
    for i in range(len(solution[0])):
        if len(set(get_row(solution, (i, 0)))) == 9 and len(set(get_col(solution, (0, i)))) == 9 and "." not in set(get_row(solution, (i,0))):
            for row in range(0,7,3):
                for col in range(0,7,3):
                    if len(set(get_block(solution,(row,col))))==9:
                        check = True
                    else:
                        return False     
        else: 
            return False
    return check



def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    table_withNumbers= [i%9 for i in range(1,82)]
    table = group(table_withNumbers, 9)
    counter_of_row = 0
    for row in table:
        for num in range(9):
            if counter_of_row % 3 == 0:
                row[num] = str(int((row[num] + counter_of_row/3) % 9))
            elif counter_of_row <3:
                row[num] = str(int((row[num]+3*counter_of_row)%9))
            elif counter_of_row <6:
                row[num] = str(int(((row[num]+3*counter_of_row)+1)%9))
            elif counter_of_row <9:
                row[num] = str(int(((row[num]+3*counter_of_row)+2)%9))
            if row[num] == '0':
                row[num] = '9'
        counter_of_row += 1 
    import random
    for i in range(20):
        i=random.randint(0,8)
        if i%3==2:
            table[i], table[i-1] = table[i-1], table[i]
        elif i%3==1:
            table[i+1], table[i-1] = table[i-1], table[i+1]
        else:
            table[i], table[i+1] = table[i+1], table[i]
    n=0
    while n<(81-N):
        row = random.randint(0,8)
        col = random.randint(0,8)
        if table[row][col] != ".":
            table[row][col] = "."
            n += 1
    return table
               



if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)