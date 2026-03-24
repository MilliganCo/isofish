# abilities.py

class Ability:
    def __init__(self, name, level=1, max_level=5, description=""):
        self.name = name
        self.level = level
        self.max_level = max_level
        self.description = description

    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
            return True
        return False

    def get_effect(self):
        # Простой эффект: базовый множитель увеличивается на 20% за каждый уровень выше 1
        return 1 + (self.level - 1) * 0.2

def create_initial_abilities():
    # Начальный набор способностей игрока
    return {
        "Fishing": Ability("Fishing", level=1, max_level=5, description="Increases fish catch chance."),
        "Navigation": Ability("Navigation", level=1, max_level=3, description="Improves boat speed and maneuverability."),
        "Luck": Ability("Luck", level=1, max_level=4, description="Increases chance of rare fish."),
    }
