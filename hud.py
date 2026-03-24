# hud.py
import pygame

def render_hud(player, width, height):
    """
    Рендерит верхнюю панель (HUD) с информацией об игроке.
    Выводит Score, количество предметов в инвентаре и краткий список способностей.
    """
    surface = pygame.Surface((width, height))
    surface.fill((30, 30, 30))  # темный фон

    font = pygame.font.SysFont("Courier", 20)
    # Отображаем счет
    score_text = f"Score: {player.score}"
    score_img = font.render(score_text, True, (255, 255, 255))
    surface.blit(score_img, (10, 5))

    # Отображаем инвентарь
    inv_text = f"Inventory: {len(player.inventory)} items"
    inv_img = font.render(inv_text, True, (255, 255, 255))
    surface.blit(inv_img, (250, 5))

    # Отображаем способности
    abilities_text = "Abilities: "
    for name, ability in player.abilities.items():
        abilities_text += f"{name}(Lv.{ability.level})  "
    abilities_img = font.render(abilities_text, True, (255, 255, 255))
    surface.blit(abilities_img, (10, 30))

    return surface
