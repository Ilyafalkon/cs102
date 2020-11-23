import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0 for i in range(self.cols)] for i in range(self.rows)]
        if randomize:
            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    if random.randint(0, 1) == 1:
                        grid[row][col] = 1
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        for row in range(cell[0] - 1, cell[0] + 2):
            for col in range(cell[1] - 1, cell[1] + 2):
                if (
                    cell != (row, col)
                    and row < len(self.curr_generation)
                    and col < len(self.curr_generation[0])
                    and row != -1
                    and col != -1
                ):
                    neighbours.append(self.curr_generation[row][col])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = [[0 for i in range(self.cols)] for i in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                alive_cells = sum(self.get_neighbours((row, col)))
                if alive_cells == 3 or (alive_cells == 2 and self.curr_generation[row][col] == 1):
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
        self.curr_generation = list(new_grid)
        return self.curr_generation

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if not self.max_generations:
            return False
        elif self.generations < self.max_generations:
            return False
        return True

    @property
    def is_changing(self) -> bool:
        if self.prev_generation == self.curr_generation:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        grid = []
        path = pathlib.Path(filename)
        with path.open() as f:
            for line in f:
                if "1" in line or "0" in line:
                    grid.extend([[int(c) for c in line if c in "10"]])
        life = GameOfLife((len(grid), len(grid[0])))
        life.curr_generation = grid
        return life

    def save(self, filename: pathlib.Path) -> None:
        path = pathlib.Path(filename)
        with path.open("w") as f:
            for row in self.curr_generation:
                for col in row:
                    f.write(str(col))
                f.write("\n")
