import random
import math

class VoxelWorld:
    def __init__(self, width, height, depth):
        """
        3D-массив (x,y,z).
        self.voxels[x][y][z] = None или словарь:
          {
            'solid': True,
            'char': символ ASCII,
            'color': (R,G,B)
          }
        """
        self.width = width
        self.height = height
        self.depth = depth

        # Для анимации волн
        self.time_accumulator = 0.0

        # Создаём пустую структуру
        self.voxels = [
            [
                [None for _ in range(depth)]
                for _ in range(height)
            ]
            for _ in range(width)
        ]
        self.generate_world()

    def generate_world(self):
        """
        Генерация:
          - нижняя часть: вода ('~')
          - острова: '@'
          - остальное: пусто
        У каждой воды и земли свой цвет.
        """
        water_level = self.depth // 3

        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    if z < water_level:
                        # вода
                        self.voxels[x][y][z] = {
                            'solid': True,
                            'char': '~',
                            # начальный цвет воды (сине-зелёный)
                            'color': (0, 80, 200)
                        }
                    else:
                        # воздух
                        self.voxels[x][y][z] = None

        # "острова"
        for _ in range(300):
            ix = random.randint(0, self.width - 1)
            iy = random.randint(0, self.height - 1)
            iz = random.randint(water_level, self.depth - 1)
            self.voxels[ix][iy][iz] = {
                'solid': True,
                'char': '@',
                'color': (0, 200, 0)  # зелёный
            }

    def update_world(self, dt):
        """
        Анимация «жизни озера»:
        - время накапливаем
        - воду слегка колеблем, меняя цвет
        """
        self.time_accumulator += dt

        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    v = self.voxels[x][y][z]
                    if v and v['char'] == '~':
                        # волна = sin(...)
                        wave = math.sin(self.time_accumulator * 1.5 + x*0.3 + y*0.2)
                        # Меняем яркость воды
                        base_blue = 180
                        delta = int(50 * wave)
                        # Цвет колеблется между (0, 80, 130) и (0, 80, 230) примерно
                        blue = max(0, min(255, base_blue + delta))
                        v['color'] = (0, 80, blue)
