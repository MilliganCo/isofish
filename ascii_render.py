import pygame
from settings import Settings

def iso_transform(x, y, z, buf_width, buf_height, tile_w, tile_h,
                  y_offset=0, camera_x=0, camera_y=0):
    """
    Преобразует координаты (x, y, z) в координаты ASCII-буфера,
    учитывая позицию камеры (camera_x, camera_y).
    """
    dx = x - camera_x
    dy = y - camera_y
    buf_x = (dx - dy) * tile_w + (buf_width // 2)
    buf_y = (dx + dy) * tile_h - z * tile_h + (buf_height // 4) + y_offset
    return int(buf_x), int(buf_y)

def compute_depth(x, y, z):
    """
    Возвращает индекс глубины (0..MAX_DEPTH-1) для данного вокселя.
    Здесь используем просто значение z.
    """
    dist = z
    if dist < 0:
        dist = 0
    if dist > Settings.MAX_DEPTH - 1:
        dist = Settings.MAX_DEPTH - 1
    return int(dist)

def pick_symbol_and_color(base_char, base_color, depth_idx):
    """
    На основании глубины (depth_idx) выбирает итоговый символ и затемнённый цвет.
    """
    symbol = Settings.DEPTH_SYMBOLS.get(depth_idx, base_char)
    dark_coeff = Settings.DEPTH_DARKEN.get(depth_idx, 0.1)
    r, g, b = base_color
    r = int(r * dark_coeff)
    g = int(g * dark_coeff)
    b = int(b * dark_coeff)
    return symbol, (r, g, b)

def render_voxel_world_ascii(world, buf_width, buf_height,
                             tile_w=2, tile_h=1, y_offset=0,
                             camera_x=0, camera_y=0):
    """
    Генерирует ASCII-буфер, учитывая смещение камеры (camera_x, camera_y),
    чтобы игрок оставался в центре.
    """
    ascii_buf = [[(' ', (0, 0, 0)) for _ in range(buf_width)] for _ in range(buf_height)]
    w = len(world.voxel_world.voxels)
    h = len(world.voxel_world.voxels[0])
    d = len(world.voxel_world.voxels[0][0])

    for z in range(d):
        for y in range(h):
            for x in range(w):
                voxel = world.voxel_world.voxels[x][y][z]
                if not voxel or not voxel.get('solid', False):
                    continue
                buf_x, buf_y = iso_transform(x, y, z,
                                             buf_width, buf_height,
                                             tile_w, tile_h,
                                             y_offset,
                                             camera_x, camera_y)
                if 0 <= buf_x < buf_width and 0 <= buf_y < buf_height:
                    depth_idx = compute_depth(z, y, z)  # упрощённый вариант
                    final_char, final_color = pick_symbol_and_color(voxel['char'], voxel['color'], depth_idx)
                    ascii_buf[buf_y][buf_x] = (final_char, final_color)

    # Отрисуем всех рыб
    for fish in world.fish_population:
        fx, fy = iso_transform(fish.x, fish.y, fish.z,
                               buf_width, buf_height,
                               tile_w, tile_h,
                               y_offset, camera_x, camera_y)
        if 0 <= fx < buf_width and 0 <= fy < buf_height:
            ch, ccol = fish.get_render_data()
            ascii_buf[fy][fx] = (ch, ccol)

    return ascii_buf

def overlay_player(ascii_buf, player, buf_width, buf_height,
                   tile_w=2, tile_h=1, y_offset=0,
                   camera_x=0, camera_y=0):
    """
    Накладывает лодку игрока на ASCII-буфер, используя iso_transform с учётом камеры.
    """
    char, color = player.get_render_data()
    buf_x, buf_y = iso_transform(player.x, player.y, player.z,
                                 buf_width, buf_height,
                                 tile_w, tile_h,
                                 y_offset,
                                 camera_x, camera_y)
    if 0 <= buf_x < buf_width and 0 <= buf_y < buf_height:
        ascii_buf[buf_y][buf_x] = (char, color)
    return ascii_buf

def render_ascii_surface(ascii_buf, font_near, font_far):
    """
    Превращает ASCII-буфер в Surface для отображения на экране.
    """
    h = len(ascii_buf)
    w = len(ascii_buf[0]) if h > 0 else 0

    line_height_near = font_near.get_linesize()
    line_height_far = font_far.get_linesize()
    line_height = max(line_height_near, line_height_far)
    char_w_near = int(line_height_near * 0.6)
    char_w_far = int(line_height_far * 0.6)
    char_w = max(char_w_near, char_w_far)

    surf_w = w * char_w
    surf_h = h * line_height
    surface = pygame.Surface((surf_w, surf_h))
    surface.fill((0, 0, 0))

    for row_idx in range(h):
        for col_idx in range(w):
            ch, (r, g, b) = ascii_buf[row_idx][col_idx]
            if ch == ' ':
                continue
            if ch in ('.', ',', '`', '*'):
                font = font_far
            else:
                font = font_near
            glyph = font.render(ch, True, (r, g, b))
            x_px = col_idx * char_w
            y_px = row_idx * line_height
            surface.blit(glyph, (x_px, y_px))
    return surface
