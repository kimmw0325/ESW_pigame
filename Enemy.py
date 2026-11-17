class Enemy:
    def __init__(self, x, y, direction, distance, enemy_type):
        self.x = x
        self.y = y
        self.radius = 8
        self.direction = direction
        self.distance = distance
        self.enemy_type = enemy_type

    def bounds(self):
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )