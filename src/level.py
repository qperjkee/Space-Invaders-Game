import random
from .utils import collide
from .entities import Enemy
from .bonus import Bonus
from .constants import ENEMY_COLORS_BY_LEVELS, SPAWN_OFFSETS


class Level:
    def __init__(self):
        self.level = 0
        self.wave_length = 5
        self.wave_growth = 3

    def increase_level(self):
        self.level += 1
        self.wave_length += self.wave_growth

    def add_score(self, score):
        if self.level >= 2:
            bonus = 1000 + (self.level - 2) * 500
            score += bonus
        return score
    
    def create_enemies(self, enemies, WIDTH):
        for _ in range(self.wave_length):
            self.y_min = -1500 if self.level < 3 else -2000 - (self.level - 3) * 100

            enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(self.y_min, -100), random.choice(ENEMY_COLORS_BY_LEVELS[min(self.level, len(ENEMY_COLORS_BY_LEVELS))]))

            move_offset = SPAWN_OFFSETS.get(enemy.color, SPAWN_OFFSETS["default"])

            if enemy.x <= 100:
                enemy.x += move_offset
            elif enemy.x >= WIDTH - 150:
                enemy.x -= move_offset

            for other_enemy in enemies:
                if collide(enemy, other_enemy):
                    enemy.y -= 100

            enemies.append(enemy)

        return enemies

    def create_bonus(self, WIDTH, bonus_obj):
        bonus_type = random.choice(list(bonus_obj.avaliable_bonuses.keys()))
        bonus = Bonus(random.randrange(50, WIDTH - 100), random.randrange(self.y_min, -100), bonus_type, bonus_obj.avaliable_bonuses)
        return bonus