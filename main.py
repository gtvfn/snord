import pygame
from game.snake import Snake
from game.apple import Apple
import game.utils as ut


def main():
    word = ut.get_word()
    word_letters = list(word)
    pygame.init()
    screen = ut.create_screen()
    clock = pygame.time.Clock()
    snake = Snake()
    snake.set_word(word_letters)
    apple = Apple()
    apple.set_letter(word_letters[len(snake.word)])
    apple.generate_apple(snake.body)
    last_move = 0
    running = True
    won_game = False
    font = pygame.font.SysFont("Bree", 30)

    while running:
        if not won_game:
            ut.movement(snake)
            won_game = ut.handle_apple_eating(snake, apple, word_letters)
            last_move = ut.maybe_move(snake, last_move)
            ut.update_screen(snake, apple, screen, font)

        else:
            ut.win_message(screen, word)

        running = ut.handle_events() and ut.check_lose(snake)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
