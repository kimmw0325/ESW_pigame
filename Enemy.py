class Enemy:
    def __init__(self, x, y, direction, distance):
        self.x = x
        self.y = y
        self.radius = 8
        self.direction = direction
        self.distance = distance

    def bounds(self):
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )