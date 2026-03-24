import math


def grid_to_iso_3d(x, y, z, tile_width, tile_height, perspective=0.003):
    """
    Преобразует координаты (x, y) и высоту z в «псевдо-3D» изометрические координаты.

    x, y: координаты клетки
    z: высота (или глубина), для имитации рельефа
    tile_width, tile_height: размеры «тайла» в пикселях
    perspective: коэффициент перспективы (чем больше, тем сильнее искажение)
    """
    # Базовая изометрическая проекция
    iso_x = (x - y) * tile_width / 2
    iso_y = (x + y) * tile_height / 2

    # Смещаем по высоте (z), например, чтобы "волны" выглядели приподнятыми
    iso_y -= z * tile_height

    # Простая перспектива: при большем z объект становится меньше
    # scale = 1 / (1 + perspective * z), чем больше z, тем сильнее «уменьшение».
    scale = 1.0 / (1.0 + perspective * z)
    iso_x *= scale
    iso_y *= scale

    return iso_x, iso_y
