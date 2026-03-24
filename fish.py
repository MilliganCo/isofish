# fish.py
import random
import math

FISH_TYPES = [
    {
        "name": "Arcane Eel",       # Волшебный угорь
        "value": 15,
        "color": (200, 0, 255)      # фиолетово-розовый
    },
    {
        "name": "Lava Carp",        # Лавовый карп
        "value": 20,
        "color": (255, 100, 0)      # ярко-оранжевый
    },
    {
        "name": "Storm Whale",      # Штормовой кит
        "value": 40,
        "color": (0, 200, 255)      # голубой
    },
    {
        "name": "Crystal Koi",      # Кристальный карп
        "value": 25,
        "color": (180, 255, 255)    # нежный бирюзовый
    },
]

class Fish:
    def __init__(self, name, x, y, z, value, color):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.value = value
        self.color = color

        self.dx = random.uniform(-0.1, 0.1)
        self.dy = random.uniform(-0.1, 0.1)
        self.dz = 0

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        if random.random() < 0.01:
            self.dx = random.uniform(-0.1, 0.1)
            self.dy = random.uniform(-0.1, 0.1)

    def get_render_data(self):
        # Символ рыбы
        return ("*", self.color)

    def distance_to(self, other_x, other_y):
        return math.hypot(self.x - other_x, self.y - other_y)
