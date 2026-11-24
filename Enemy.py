class Enemy:
    def __init__(self, x, y, direction, distance, enemy_type, *, spiral_angle=None):
        self.x = x
        self.y = y
        self.direction = direction
        self.distance = distance
        self.enemy_type = enemy_type
        self.spiral_angle = spiral_angle
        self.radius = 8 if spiral_angle is None else 10

    def bounds(self):
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )