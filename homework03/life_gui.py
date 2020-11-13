import argparse
import sys

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI

parser = argparse.ArgumentParser(
    description="This is graphic version Game Of Life. Write the width, heigth and cell size of the gametable"
)

parser.add_argument("--width")
parser.add_argument("--heigth")
parser.add_argument("--cell_size")
args = parser.parse_args()


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.height = self.life.rows * self.cell_size
        self.width = self.life.cols * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 0:
                    colour = "white"
                else:
                    colour = "green"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(colour),
                    (self.cell_size * col, self.cell_size * row, self.cell_size, self.cell_size),
                )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        pause = False
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pause = True
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            while pause:
                for event in pygame.event.get():
                    if event.type == QUIT: #type: ignore
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        pause = False
                    elif event.type == pygame.MOUSEBUTTONUP:
                        position = pygame.mouse.get_pos()
                        col, row = int(position[0] / self.cell_size), int(
                            position[1] / self.cell_size
                        )
                        if self.life.curr_generation[row][col] == 1:
                            self.life.curr_generation[row][col] = 0
                        else:
                            self.life.curr_generation[row][col] = 1
                        self.draw_grid()
                        self.draw_lines()
                        pygame.display.flip()
            self.life.step()
            clock.tick(self.speed)
        pygame.quit()


if type(args.width) == str and type(args.heigth) == str and type(args.cell_size) == str:
    rows = int(int(args.heigth) / int(args.cell_size))
    cols = int(int(args.width) / int(args.cell_size))
    life = GameOfLife((rows, cols))
    ui = GUI(life, cell_size=int(args.cell_size))
    ui.run()

if __name__ == '__main__':
    life = GameOfLife((20,20))
    ui = GUI(life, cell_size = 40)
    ui.run()