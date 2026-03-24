import random


def create_initial_grid(width, height):
    """
    Создаём список списков, где каждая ячейка – кортеж (символ, z).
    Пример: ('~', 0.2) — клетка воды с высотой 0.2.
    """
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            # Тип тайла (вода/волна/рыбка)
            symbol = random.choice(['~', '.', '*'])
            # Случайная высота (0…2), можно интерпретировать как высоту волны
            z = random.uniform(0, 2) if symbol != '.' else random.uniform(0, 1)
            row.append((symbol, z))
        grid.append(row)
    return grid


def update_automata(grid):
    """
    Обновляет клеточный автомат.
    Для примера: у небольшого процента клеток слегка меняется z,
    а иногда и сам символ.
    """
    new_grid = []
    for row in grid:
        new_row = []
        for (cell, z) in row:
            # С вероятностью 5% слегка меняем высоту
            if random.random() < 0.05:
                # Колебание волны
                z += random.uniform(-0.2, 0.2)
                z = max(0, min(z, 3))  # ограничим от 0 до 3

            # С вероятностью 1% меняем сам символ (например, появляется/исчезает рыбка)
            if random.random() < 0.01:
                cell = random.choice(['~', '.', '*'])

            new_row.append((cell, z))
        new_grid.append(new_row)
    return new_grid
