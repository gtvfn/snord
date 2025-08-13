import pygame
import requests
import game.config as cfg
from random import randint, choice


def maybe_move(snake, last_move: int) -> int:
    cur_time = pygame.time.get_ticks()

    if cur_time - last_move > cfg.MOVE_DELAY:
        snake.move()
        return cur_time

    return last_move


def create_screen():
    return pygame.display.set_mode(
        (
            cfg.WIDTH * cfg.CELL_SIZE,
            cfg.HEIGHT * cfg.CELL_SIZE,
        )
    )


def is_inside(pos: tuple[int, int]) -> bool:
    x, y = pos
    return 0 <= x <= cfg.WIDTH - 1 and 0 <= y <= cfg.HEIGHT - 1


def check_collision(body) -> bool:
    return body[0] not in body[1:]


def check_lose(snake) -> bool:
    if not is_inside(snake.body[0]) or not check_collision(snake.body):
        print("You lost :(")
        return False

    return True


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True


def check_eat(snake_head: tuple, apple_pos: tuple) -> bool:
    return snake_head == apple_pos


def handle_apple_eating(snake, apple, word: list) -> None:
    if check_eat(snake.body[0], apple.pos):
        snake.grow()
        index = len(snake.word)

        if index < len(word):
            snake.word.append(word[index])

            if index + 1 < len(word):
                apple.set_letter(word[index + 1])
                apple.generate_apple(snake.body)
            else:
                apple.pos = (-1, -1)
                return True
    return False


def movement(snake) -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        snake.set_direction(cfg.UP)

    elif keys[pygame.K_a]:
        snake.set_direction(cfg.LEFT)

    elif keys[pygame.K_s]:
        snake.set_direction(cfg.DOWN)

    elif keys[pygame.K_d]:
        snake.set_direction(cfg.RIGHT)


def update_screen(snake, apple, screen, font) -> None:
    screen.fill((0, 0, 0))
    apple.draw_apple(screen, font)
    snake.draw_snake(screen, font)
    pygame.display.flip()


def draw_letter(screen, lttr: str, font, rect) -> None:
    letter = font.render(lttr, True, (255, 255, 255))
    letter_rect = letter.get_rect(center=rect.center)
    screen.blit(letter, letter_rect)


def get_word() -> None:
    response = requests.get(
        f"https://api.datamuse.com/words?sp={randint(5, 7)*'?'}&max=500"
    )
    words = response.json()

    if not words:
        return None

    return choice(words)["word"]


def win_message(screen, word: str) -> None:
    font = pygame.font.SysFont("FF Kava", 70)
    screen.fill((0, 0, 0))

    win_text = font.render("You Won!", True, (255, 255, 255))
    win_rect = win_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 - 80)
    )

    word_text = font.render(word, True, (255, 255, 255))
    word_rect = word_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + 20)
    )

    screen.blit(win_text, win_rect)
    screen.blit(word_text, word_rect)
    pygame.display.flip()
