# console.py
import pygame

def render_console(player, width, height):
    """
    Рендерит нижнюю панель – игровую консоль/чат, выводящую последние сообщения игрока.
    """
    surface = pygame.Surface((width, height))
    surface.fill((10, 10, 10))  # очень темный фон

    font = pygame.font.SysFont("Courier", 18)
    # Выведем последние 5 сообщений
    messages = player.messages[-5:]
    for i, msg in enumerate(messages):
        msg_img = font.render(msg, True, (200, 200, 200))
        surface.blit(msg_img, (10, i * 22))
    return surface
