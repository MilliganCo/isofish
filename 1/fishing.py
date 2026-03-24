import random

class FishingSystem:
    def __init__(self, voxel_world):
        self.voxel_world = voxel_world
        self.catch_chance = 0.3  # базовый шанс поймать рыбу
        # можно хранить состояние удочки, таймер, и т.д.

    def cast_line(self, x, y, z):
        """
        Игрок пытается ловить рыбу в координатах (x, y, z).
        Допустим, это поверхность воды. Проверяем, есть ли рыба.
        """
        voxel = self.voxel_world.voxels[x][y][z]
        if voxel and voxel['type'] == 'water':
            # 10% шанс, что в этом вокселе есть рыба
            if random.random() < self.catch_chance:
                print("You caught a fish!")
                # Можно «вытащить» рыбу из этого места, изменить тип и т.д.
            else:
                print("No luck this time...")
        else:
            print("This is not water. You can't fish here.")
