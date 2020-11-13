import argparse
import curses
import sys

from life import GameOfLife
from ui import UI

parser = argparse.ArgumentParser(
    description="This is console version of Game Of Life. Write the number of rows, cols and max generation"
)

parser.add_argument("--rows")
parser.add_argument("--cols")
parser.add_argument("--max_generations")
args = parser.parse_args()


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        for row in range(self.life.rows + 2):
            for col in range(self.life.cols + 2):
                if row == 0 or row == self.life.rows + 1:
                    if col == 0 or col == self.life.cols + 1:
                        screen.addstr(row, col, "+")
                    else:
                        screen.addstr(row, col, "-")
                else:
                    if col == 0 or col == self.life.cols + 1:
                        screen.addstr(row, col, "|")
                    else:
                        screen.addstr(row, col, " ")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    screen.addstr(row + 1, col + 1, "*")

    def run(self) -> None:
        screen = curses.initscr()
        curses.wrapper(self.draw_borders)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            screen.refresh()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            screen.getch()
        curses.endwin()


if type(args.rows) == str and type(args.cols) == str and type(args.max_generations) == str:
    life = GameOfLife((int(args.rows), int(args.cols)), max_generations=int(args.max_generations))
    ui = Console(life)
    ui.run()
