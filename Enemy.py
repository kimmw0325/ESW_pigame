class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8

    def bounds(self):
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )