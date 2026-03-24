import random
import math
from fish import Fish, FISH_TYPES

class VoxelWorld:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        # 3D-массив вокселей
        self.voxels = [
            [
                [None for _ in range(depth)]
                for _ in range(height)
            ]
            for _ in range(width)
        ]
        self.generate_voxels()

    def generate_voxels(self):
        water_level = self.depth // 3
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    if z < water_level:
                        # Вода
                        self.voxels[x][y][z] = {
                            'solid': True,
                            'char': '~',
                            'color': (0, 80, 200)
                        }
                    else:
                        self.voxels[x][y][z] = None

        # Генерация "островов" (земля)
        for _ in range(300):
            ix = random.randint(0, self.width - 1)
            iy = random.randint(0, self.height - 1)
            iz = random.randint(water_level, self.depth - 1)
            self.voxels[ix][iy][iz] = {
                'solid': True,
                'char': '@',
                'color': (0, 200, 0)
            }

        # Добавляем водоросли в воде (примерно 2% ячеек)
        for x in range(self.width):
            for y in range(self.height):
                for z in range(water_level):
                    if random.random() < 0.02:
                        self.voxels[x][y][z] = {
                            'solid': True,
                            'char': '!',
                            'color': (0, 180, 0)
                        }

    def update_world(self, dt):
        # Место для анимации воды или других эффектов
        pass

class GameWorld:
    def __init__(self):
        # Создаём воксельный мир
        self.voxel_world = VoxelWorld(width=50, height=50, depth=20)
        self.fish_population = []
        self.weather = "clear"
        # Спауним начальные рыбы
        self.spawn_initial_fish()

    def spawn_initial_fish(self):
        water_level = self.voxel_world.depth // 3
        fish_count = 20
        for _ in range(fish_count):
            fish_type = random.choice(FISH_TYPES)
            x = random.randint(0, self.voxel_world.width - 1)
            y = random.randint(0, self.voxel_world.height - 1)
            z = random.randint(0, water_level - 1)
            # Создаём рыбу из случайного типа
            fish = Fish(
                name=fish_type["name"],
                x=x,
                y=y,
                z=z,
                value=fish_type["value"],
                color=fish_type["color"]
            )
            self.fish_population.append(fish)

    def update(self, dt):
        self.voxel_world.update_world(dt)
        self.update_fish(dt)

    def update_fish(self, dt):
        # Обновляем положение всех рыб
        for fish in self.fish_population:
            fish.update(dt)

        # Иногда рыба исчезает
        self.fish_population = [
            f for f in self.fish_population if random.random() > 0.0005
        ]

        # Иногда появляются новые рыбы (пример)
        if random.random() < 0.001:
            water_level = self.voxel_world.depth // 3
            x = random.randint(0, self.voxel_world.width - 1)
            y = random.randint(0, self.voxel_world.height - 1)
            z = random.randint(0, water_level - 1)
            # Для "новой" рыбы можно брать случайный тип, либо указать свой
            fish_type = random.choice(FISH_TYPES)
            new_fish = Fish(
                name=fish_type["name"],
                x=x,
                y=y,
                z=z,
                value=fish_type["value"],
                color=fish_type["color"]
            )
            self.fish_population.append(new_fish)

        # Проверяем столкновения (рыбы поедают друг друга)
        eaten = set()
        for i in range(len(self.fish_population)):
            if i in eaten:
                continue
            f1 = self.fish_population[i]
            for j in range(i+1, len(self.fish_population)):
                if j in eaten:
                    continue
                f2 = self.fish_population[j]
                dist = f1.distance_to(f2.x, f2.y)
                if dist < 0.5:  # столкнулись
                    if f1.value > f2.value:
                        f1.value += f2.value
                        eaten.add(j)
                    elif f2.value > f1.value:
                        f2.value += f1.value
                        eaten.add(i)
                        break
        # Удаляем съеденных рыб
        self.fish_population = [
            f for idx, f in enumerate(self.fish_population) if idx not in eaten
        ]
