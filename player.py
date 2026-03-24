import math
import random

class Player:
    def __init__(self, x, y, z, world_width=50, world_height=50):
        self.x = x
        self.y = y
        self.z = z
        self.world_width = world_width
        self.world_height = world_height

        self.inventory = []
        self.score = 0
        self.abilities = {}
        self.messages = []

        self.speed = 3.0

        # Логика «кольцевой» мини-игры
        self.is_fishing = False              # Флаг, идёт ли ловля
        self.fishing_target_fish = None      # Какая рыба ловится
        self.fishing_progress = 0.0          # Текущая шкала (0..100)

        # Кольцо игрока (два радиуса: внутренний и внешний)
        self.player_inner = 20.0
        self.player_outer = 30.0
        # Скорости изменения радиусов игрока
        self.player_inner_speed = -5.0
        self.player_outer_speed = -8.0

        # Кольцо рыбы (два радиуса)
        self.fish_inner = 50.0
        self.fish_outer = 70.0
        # Хаотичные скорости изменения радиусов рыбы
        self.fish_inner_speed = random.uniform(-10, -3)
        self.fish_outer_speed = random.uniform(-10, 10)

    def move(self, dx, dy, dz):
        """Движение игрока с учётом скорости и ограничения мира."""
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.z += dz * self.speed
        if self.x < 0:
            self.x = 0
        if self.x >= self.world_width:
            self.x = self.world_width - 1
        if self.y < 0:
            self.y = 0
        if self.y >= self.world_height:
            self.y = self.world_height - 1

    def update(self, dt):
        """Каждый кадр обновляем состояние мини-игры рыбалки (если идёт ловля)."""
        if not self.is_fishing or not self.fishing_target_fish:
            return

        # Кольцо игрока
        self.player_inner += self.player_inner_speed * dt
        self.player_outer += self.player_outer_speed * dt
        if self.player_inner < 1:
            self.player_inner = 1
        if self.player_outer < self.player_inner + 5:
            self.player_outer = self.player_inner + 5

        # Кольцо рыбы
        self.fish_inner += self.fish_inner_speed * dt
        self.fish_outer += self.fish_outer_speed * dt
        # Периодически меняем скорости хаотично
        if random.random() < 0.02:
            self.fish_inner_speed = random.uniform(-10, 10)
        if random.random() < 0.02:
            self.fish_outer_speed = random.uniform(-10, 10)
        # Следим, чтобы внешнее кольцо рыбы не стало меньше внутреннего
        if self.fish_outer < self.fish_inner + 5:
            self.fish_outer = self.fish_inner + 5

        # Считаем, насколько хорошо пересекаются кольца игрока и рыбы
        overlap_ratio = self.compute_rings_overlap(
            (self.player_inner, self.player_outer),
            (self.fish_inner, self.fish_outer)
        )

        # Если пересечение велико – растём в прогрессе, иначе падаем
        if overlap_ratio > 0.2:
            self.fishing_progress += overlap_ratio * 30 * dt
        else:
            self.fishing_progress -= 15 * dt

        # Ограничиваем шкалу (0..100) и проверяем успех/провал
        if self.fishing_progress <= 0:
            self.fishing_progress = 0
            self.messages.append("Рыба сорвалась!")
            self.is_fishing = False
            self.fishing_target_fish = None
        elif self.fishing_progress >= 100:
            self.fishing_progress = 100
            self.catch_fish(self.fishing_target_fish)
            self.is_fishing = False
            self.fishing_target_fish = None

    def compute_rings_overlap(self, ringA, ringB):
        """
        ringA = (A_inner, A_outer)
        ringB = (B_inner, B_outer)
        Возвращаем долю перекрытия относительно ширины кольца A.
        """
        A_in, A_out = ringA
        B_in, B_out = ringB

        overlap_start = max(A_in, B_in)
        overlap_end = min(A_out, B_out)
        overlap_length = overlap_end - overlap_start
        if overlap_length < 0:
            overlap_length = 0

        widthA = A_out - A_in
        if widthA <= 0:
            return 0.0

        return overlap_length / widthA

    def start_fishing(self, fish):
        """Инициализация мини-игры ловли рыбы."""
        self.is_fishing = True
        self.fishing_target_fish = fish
        self.fishing_progress = 0.0
        self.messages.append(f"Начали ловить: {fish.name}")

        # Кольцо игрока
        self.player_inner = 20.0
        self.player_outer = 35.0
        self.player_inner_speed = -5.0
        self.player_outer_speed = -8.0

        # Кольцо рыбы
        self.fish_inner = 30.0
        self.fish_outer = 50.0
        self.fish_inner_speed = -5.0
        self.fish_outer_speed = 5.0

    def catch_fish(self, fish):
        """Добавляем рыбу в инвентарь, увеличиваем счёт."""
        self.inventory.append(fish)
        self.score += fish.value
        self.messages.append(f"Поймана рыба: {fish.name} на {fish.value} очков")

    def get_render_data(self):
        """Возвращаем символ и цвет для ASCII-рендера лодки."""
        return ("B", (255, 255, 0))
