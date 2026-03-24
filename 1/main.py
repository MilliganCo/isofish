import pygame
import sys

from voxel_world import VoxelWorld

def render_voxel_world_ascii(voxel_world, buf_width, buf_height, tile_w=2, tile_h=1, y_offset=10):
    """
    Генерирует ASCII-«изометрию» по вокселям + цвет для каждого символа.
    Возвращает 2D-массив (buf_height x buf_width) из кортежей (char, (R,G,B)).
    """
    # Подготовим 2D-массив: в каждой ячейке (char, color)
    # Изначально всё - пробелы с чёрным цветом
    ascii_buffer = [[(' ', (0,0,0)) for _ in range(buf_width)] for _ in range(buf_height)]

    # Перебираем воксели
    for z in range(voxel_world.depth):
        for y in range(voxel_world.height):
            for x in range(voxel_world.width):
                v = voxel_world.voxels[x][y][z]
                if not v or not v['solid']:
                    continue

                # Псевдо-изометрические координаты
                iso_x = (x - y) * tile_w + (buf_width // 2)
                iso_y = (x + y) * tile_h + (voxel_world.depth - 1 - z) * tile_h + y_offset

                # Проверка границ
                if 0 <= iso_x < buf_width and 0 <= iso_y < buf_height:
                    ascii_buffer[iso_y][iso_x] = (v['char'], v['color'])

    return ascii_buffer


def main():
    pygame.init()

    # Окно
    screen_width, screen_height = 2200, 1300
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Colored ASCII Voxel Lake")

    # Создаём более широкое поле
    voxel_world = VoxelWorld(width=50, height=50, depth=20)

    # ASCII-буфер
    ascii_buf_width = 250
    ascii_buf_height = 120

    # Шрифт
    font = pygame.font.SysFont("Courier", 18, bold=False)

    clock = pygame.time.Clock()

    while True:
        dt = clock.get_time() / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Обновляем мир (волны и т.д.)
        voxel_world.update_world(dt)

        # Генерируем ASCII-буфер
        ascii_buffer = render_voxel_world_ascii(
            voxel_world,
            buf_width=ascii_buf_width,
            buf_height=ascii_buf_height,
            tile_w=2,
            tile_h=1,
            y_offset=10  # опускаем всю сцену
        )

        # Создаём Surface для вывода
        line_height = font.get_linesize()
        # Предположим, на один символ по X ~ 12 пикселей
        char_width = 12

        ascii_surf_width = ascii_buf_width * char_width
        ascii_surf_height = ascii_buf_height * line_height

        ascii_surface = pygame.Surface((ascii_surf_width, ascii_surf_height))
        ascii_surface.fill((0, 0, 0))

        # Рендерим построчно, но теперь у нас разные цвета на каждый символ
        for row_idx, row in enumerate(ascii_buffer):
            y_px = row_idx * line_height
            x_px = 0
            for col_idx, (ch, col) in enumerate(row):
                # col — это (R,G,B)
                # Рендерим один символ
                # Можно делать render(ch, True, col), но тогда background остаётся чёрным
                # Это даёт «цветные символы» на чёрном фоне
                glyph = font.render(ch, True, col)
                ascii_surface.blit(glyph, (x_px, y_px))
                x_px += char_width

        # Масштабируем на всё окно
        scaled = pygame.transform.scale(ascii_surface, (screen_width, screen_height))
        screen.blit(scaled, (0, 0))

        pygame.display.flip()
        clock.tick(20)


if __name__ == "__main__":
    main()
