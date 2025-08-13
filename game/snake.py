from game.config import START_POS, CELL_SIZE
from game.utils import draw_letter
import pygame


pygame.init()
pygame.font.init()


class Snake:
    def __init__(self):
        self.body = [START_POS, (START_POS[0], START_POS[1] - 1)]
        self.direction = (0, 1)
        self.grow_flag = False
        self.word = []
        self.direction_changed = False

    def set_word(self, word: list) -> None:
        self.word = word[: len(self.body)]

    def move(self) -> None:
        dx, dy = self.direction
        hx, hy = self.body[0]

        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)

        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

        self.direction_changed = False

    def set_direction(self, new_direction: tuple):
        if self.direction_changed:
            return

        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction
            self.direction_changed = True

    def grow(self) -> None:
        self.grow_flag = True

    def draw_snake(self, screen: pygame, font) -> tuple:
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(
                x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                CELL_SIZE - 2, CELL_SIZE - 2
            )
            color = (0, 255, 0)
            pygame.draw.rect(screen, color, rect)

            if self.word and i < len(self.word):
                draw_letter(screen, self.word[i], font, rect)
