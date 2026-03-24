import pygame
import sys
import random
import math

from game_world import GameWorld
from player import Player
from abilities import create_initial_abilities
from ascii_render import (
    render_voxel_world_ascii,
    overlay_player,
    render_ascii_surface
)
from console import render_console
from settings import Settings

def main():
    pygame.init()
    screen_width, screen_height = 2200, 1300
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(Settings.WINDOW_TITLE)

    clock = pygame.time.Clock()

    # Панели сверху/снизу
    hud_height = 100
    console_height = 100
    game_area_height = screen_height - hud_height - console_height
    game_area_width = screen_width

    # Создаём мир и игрока
    game_world = GameWorld()
    player = Player(
        x=25, y=25, z=(game_world.voxel_world.depth // 3) - 1,
        world_width=game_world.voxel_world.width,
        world_height=game_world.voxel_world.height
    )
    player.abilities = create_initial_abilities()

    # Параметры ASCII-буфера
    ascii_buf_width = Settings.ASCII_BUFFER_W
    ascii_buf_height = Settings.ASCII_BUFFER_H
    tile_w = Settings.TILE_W
    tile_h = Settings.TILE_H
    y_offset = 5

    font_near = pygame.font.SysFont(Settings.FONT_NAME, Settings.FONT_SIZE_NEAR)
    font_far = pygame.font.SysFont(Settings.FONT_NAME, Settings.FONT_SIZE_FAR)

    # Параметры «кольцевой» мини-игры (для ловли рыбы)
    fishing_outer_radius = 100  # Большой круг
    # Сколько «подпрыгивает» кольцо рыбы
    fish_ring_pulse_speed = 25

    while True:
        dt = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Начать рыбалку (F), если рядом есть рыба
                if event.key == pygame.K_f and (not player.is_fishing):
                    # Ищем ближайшую рыбу к игроку
                    catch_dist = 2.0
                    found_fish = None
                    for f in game_world.fish_population:
                        dist = math.hypot(f.x - player.x, f.y - player.y)
                        if dist < catch_dist:
                            found_fish = f
                            catch_dist = dist
                    if found_fish:
                        player.start_fishing(found_fish)

            # Во время мини-игры ловли, можно нажимать G, чтобы поддерживать кольцо игрока
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and player.is_fishing:
                    # Вместо: player.fishing_player_ring += 6
                    # используем:
                    player.player_outer += 6

        # Нажатые клавиши для движения
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        if keys[pygame.K_w]:
            move_y -= 1
        if keys[pygame.K_s]:
            move_y += 1
        if keys[pygame.K_a]:
            move_x -= 1
        if keys[pygame.K_d]:
            move_x += 1

        # Движение игрока
        if move_x != 0 or move_y != 0:
            player.move(move_x * dt, move_y * dt, 0)

        # Обновляем мир и игрока
        game_world.update(dt)
        player.update(dt)

        # Камера
        camera_x = player.x
        camera_y = player.y

        # Генерируем ASCII
        ascii_buf = render_voxel_world_ascii(
            game_world,
            ascii_buf_width, ascii_buf_height,
            tile_w, tile_h,
            y_offset,
            camera_x, camera_y
        )
        ascii_buf = overlay_player(ascii_buf,
                                   player,
                                   ascii_buf_width, ascii_buf_height,
                                   tile_w, tile_h,
                                   y_offset,
                                   camera_x, camera_y)
        game_area_surface = render_ascii_surface(ascii_buf, font_near, font_far)
        game_area_surface = pygame.transform.scale(
            game_area_surface,
            (game_area_width, game_area_height)
        )

        # Рисуем поверх ASCII — мини-игру рыбалки (кольца, шкалу)
        if player.is_fishing and player.fishing_target_fish:
            cx, cy = 200, 200

            # Большой "фон" можно не делать, а просто нарисуем кольца
            # Сама рыба
            fish_in = int(player.fish_inner)
            fish_out = int(player.fish_outer)
            pygame.draw.circle(game_area_surface, (255, 100, 100), (cx, cy), fish_out, 2)
            pygame.draw.circle(game_area_surface, (255, 100, 100), (cx, cy), fish_in, 2)

            # Игрок
            p_in = int(player.player_inner)
            p_out = int(player.player_outer)
            pygame.draw.circle(game_area_surface, (100, 255, 100), (cx, cy), p_out, 2)
            pygame.draw.circle(game_area_surface, (100, 255, 100), (cx, cy), p_in, 2)

            # Шкала (0..100)
            # Пример: просто прямоугольник снизу от колец
            bar_w = 150
            bar_h = 10
            pygame.draw.rect(game_area_surface, (180, 180, 180),
                             (cx - bar_w // 2, cy + fish_out + 20,
                              bar_w, bar_h), 0)
            # Заполняем красным пропорцию
            fill_len = int(bar_w * (player.fishing_progress / 100.0))
            pygame.draw.rect(game_area_surface, (255, 50, 50),
                             (cx - bar_w // 2, cy + fish_out + 20,
                              fill_len, bar_h), 0)

        # Отрисуем 9 «слотов» инвентаря внизу экрана (вместе с консолью)
        console_surface = render_console(player, screen_width, console_height)
        draw_inventory_slots(console_surface, player.inventory, slot_count=9)

        # Компонуем
        final_surface = pygame.Surface((screen_width, screen_height))
        # HUD (упростим — не используем отдельный hud.py, а просто нарисуем сверху)
        hud_surface = draw_top_hud(player, screen_width, hud_height)
        final_surface.blit(hud_surface, (0, 0))
        final_surface.blit(game_area_surface, (0, hud_height))
        final_surface.blit(console_surface, (0, hud_height + game_area_height))

        screen.blit(final_surface, (0, 0))
        pygame.display.flip()

def draw_top_hud(player, width, height):
    # Упрощённо: вверху поверх фон
    surf = pygame.Surface((width, height))
    surf.fill((30, 30, 30))
    font = pygame.font.SysFont("Courier", 20)
    text = f"Score: {player.score}   Inventory: {len(player.inventory)} items  Abilities: " \
            + " ".join([f"{k}(Lv.{v.level})" for k, v in player.abilities.items()])
    timg = font.render(text, True, (255, 255, 255))
    surf.blit(timg, (10, 10))
    return surf

def draw_inventory_slots(console_surf, inventory, slot_count=9):
    """
    Рисуем 9 слотов в нижней панели (console_surf).
    Примерно по 60px на слот.
    """
    slot_w = 60
    slot_h = 60
    margin = 5
    start_x = 10
    y = console_surf.get_height() - slot_h - 5  # снизу

    for i in range(slot_count):
        x = start_x + i * (slot_w + margin)
        # Слот серым цветом
        pygame.draw.rect(console_surf, (100, 100, 100), (x, y, slot_w, slot_h), 2)
        # Если в инвентаре есть предмет i — отрисуем что-нибудь
        if i < len(inventory):
            fish = inventory[i]
            # Название рыбы — мелким шрифтом
            font = pygame.font.SysFont("Courier", 14)
            label = font.render(f"{fish.name}", True, (200, 200, 200))
            console_surf.blit(label, (x+5, y+5))

# Подменяем метод render_console, чтобы он не перетирал нижнюю часть инвентаря
# но в данном примере мы просто вызываем его до draw_inventory_slots()

if __name__ == "__main__":
    main()
