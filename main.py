import pygame
from game import Game
from levels import levels

pygame.init()
FONT = pygame.font.SysFont(None, 48)
SCREEN = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Rush Hour - Menu")


def draw_menu(level_names, selected_index):
    SCREEN.fill((50, 50, 50))
    title = FONT.render("Sélection du niveau", True, (255, 255, 255))
    title_rect = title.get_rect(center=(SCREEN.get_width() // 2, 50))
    SCREEN.blit(title, title_rect)

    for i, name in enumerate(level_names):
        color = (255, 255, 0) if i == selected_index else (255, 255, 255)
        text = FONT.render(name, True, color)
        text_rect = text.get_rect(center=(SCREEN.get_width() // 2, 120 + i * 60))
        SCREEN.blit(text, text_rect)

    pygame.display.flip()


def main_menu():
    level_names = list(levels.keys())
    selected_index = 0
    clock = pygame.time.Clock()

    while True:
        draw_menu(level_names, selected_index)
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(level_names)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(level_names)
                elif event.key == pygame.K_RETURN:
                    return levels[level_names[selected_index]]


def main():
    while True:
        level_data = main_menu()
        if level_data is None:
            break

        while True:
            game = Game(level_data)
            result = game.run()
            if result == "quit":
                return
            elif result == "menu":
                break  # Retour au menu principal
            elif result == "replay":
                continue  # Rejouer le même niveau


if __name__ == "__main__":
    main()
