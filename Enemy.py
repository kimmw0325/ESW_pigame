class Enemy:
    """An enemy moving along one lane toward the ship."""

    def __init__(self, spawn_position, direction, enemy_type, distance):
        # The TA example draws each enemy from a four-coordinate bounding box.
        self.appearance = "circle" if enemy_type == "A" else "rectangle"
        self.center = spawn_position
        self.direction = direction
        self.enemy_type = enemy_type
        self.distance = distance
        self.radius = 8

    @property
    def position(self):
        x, y = self.center
        radius = self.radius
        x, y = round(x), round(y)
        return (x - radius, y - radius, x + radius, y + radius)

    def move(self, dx, dy, distance):
        x, y = self.center
        self.center = (x - dx * distance, y - dy * distance)
        self.distance -= distance
