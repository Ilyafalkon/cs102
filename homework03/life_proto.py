import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        # Создание списка клеток
        self.create_grid()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    running = False
            self.draw_lines()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            self.get_next_generation()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        self.grid = [[0 for i in range(self.cell_width)] for i in range(self.cell_height)]
        if randomize:
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if random.randint(0, 1) == 1:
                        self.grid[row][col] = 1
        return self.grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if self.grid[row][col] == 0:
                    colour = "white"
                else:
                    colour = "green"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(colour),
                    (self.cell_size * col, self.cell_size * row, self.cell_size, self.cell_size),
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        for row in range(cell[0] - 1, cell[0] + 2):
            for col in range(cell[1] - 1, cell[1] + 2):
                if (
                    cell != (row, col)
                    and row < len(self.grid)
                    and col < len(self.grid[0])
                    and row != -1
                    and col != -1
                ):
                    neighbours.append(self.grid[row][col])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = [[0 for i in range(self.cell_width)] for i in range(self.cell_height)]
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                alive_cells = sum(self.get_neighbours((row, col)))
                if alive_cells == 3 or (alive_cells == 2 and self.grid[row][col] == 1):
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
        self.grid = list(new_grid)
        return self.grid
