import pygame
from isometric import grid_to_iso_3d


def render_grid(screen, grid, tile_width, tile_height, font):
    screen_width, screen_height = screen.get_size()

    # Чтобы сетка располагалась ближе к центру, используем смещение.
    offset_x = screen_width // 2
    offset_y = 100

    for y, row in enumerate(grid):
        for x, (cell, z) in enumerate(row):
            iso_x, iso_y = grid_to_iso_3d(x, y, z, tile_width, tile_height)
            pos_x = int(offset_x + iso_x)
            pos_y = int(offset_y + iso_y)

            # Определяем цвет в зависимости от типа клетки
            if cell == '~':
                color = (0, 100, 255)  # синяя вода
            elif cell == '.':
                color = (0, 150, 200)  # светлая волна
            elif cell == '*':
                color = (255, 215, 0)  # золотая рыбка
            else:
                color = (255, 255, 255)

            text_surface = font.render(cell, True, color)
            screen.blit(text_surface, (pos_x, pos_y))
