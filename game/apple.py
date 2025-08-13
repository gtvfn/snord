import pygame
from game.config import HEIGHT, WIDTH, CELL_SIZE
from random import choice
from game.utils import draw_letter


class Apple:
    def __init__(self):
        self.pos = None
        self.letter = None

    def set_letter(self, letter: str) -> None:
        self.letter = letter

    def generate_apple(self, body: list) -> None:
        all_cells = ((x, y) for x in range(WIDTH) for y in range(HEIGHT))
        available_cells = list(set(all_cells) - set(body))
        self.pos = choice(available_cells)

    def draw_apple(self, screen, font) -> None:
        x, y = self.pos
        rect = pygame.Rect(
            x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2
        )
        color = (255, 0, 0)
        pygame.draw.rect(screen, color, rect)

        draw_letter(screen, self.letter, font, rect)
