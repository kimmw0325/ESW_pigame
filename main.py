from PIL import Image, ImageDraw, ImageFont
import time
import random
from colorsys import hsv_to_rgb

#from Character import Character
from Joystick import Joystick
from Enemy import Enemy

joystick = Joystick()

my_image = Image.new("RGB", (joystick.width, joystick.height))
my_draw = ImageDraw.Draw(my_image)

center_x = joystick.width // 2
center_y = joystick.height // 2

for radius in (50, 90):
    my_draw.ellipse(
        (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
        outline = "#16C7F3",
        width = 2
    )

#플레이어 그리기
ship_radius = 12 
my_draw.ellipse(
    (center_x - ship_radius, center_y - ship_radius, center_x + ship_radius, center_y + ship_radius),
    fill = "white"
)

joystick.disp.image(my_image)

buttons = {
    "UP": joystick.button_U,
    "DOWN": joystick.button_D,
    "LEFT": joystick.button_L,
    "RIGHT": joystick.button_R,
    "A": joystick.button_A,
    "B": joystick.button_B,
}

directions = {
    "UP":    (0, -1),
    "DOWN":  (0, 1),
    "LEFT":  (-1, 0),
    "RIGHT": (1, 0),
}

laser_colors = {"A": "red", "B": "lime"}

screen_edges = {
    "UP":    (center_x, 0),
    "DOWN":  (center_x, joystick.height - 1),
    "LEFT":  (0, center_y),
    "RIGHT": (joystick.width - 1, center_y),
}

enemies = []
previous_time = time.monotonic()
next_spawn_at = previous_time + 1.2

aim = "UP"
previous = []
laser = None
laser_ends_at = 0
last_drawn_state = None

previous_time = time.monotonic()

while True:
    pressed = [name for name, button in buttons.items() if not button.value]
    now = time.monotonic()

    elapsed = now - previous_time # 경과 시간
    previous_time = now 

    for enemy in enemies:
        enemy.distance -= 16 * elapsed # 적 이동속도
        dx, dy = directions[enemy.direction]
        enemy.x = center_x + dx * enemy.distance
        enemy.y = center_y + dy * enemy.distance

    enemies = [
        enemy for enemy in enemies
        if enemy.distance > ship_radius + enemy.radius
    ]

    if now >= next_spawn_at:
        direction = random.choice(list(directions))
        spawn_x, spawn_y = screen_edges[direction]
        distance = abs(spawn_x - center_x) + abs(spawn_y - center_y)
        enemy_type = random.choice(("A", "B"))
        enemies.append(Enemy(spawn_x, spawn_y, direction, distance, enemy_type))
        next_spawn_at = now + 1.5 # 적 스폰 주기 (현재 1.5초)

    for direction in directions:
        if direction in pressed:
            aim = direction
            break

    for button_name, color in laser_colors.items():
        if button_name in pressed and button_name not in previous:
            laser = (aim, color)
            laser_ends_at = now + 0.15
            break

    if laser is not None and now >= laser_ends_at:
        laser = None

    enemy_state = tuple(
        (enemy.enemy_type, tuple(round(value) for value in enemy.bounds()))
        for enemy in enemies
    )
    screen_state = (aim, laser, enemy_state)

    if screen_state != last_drawn_state:
        frame = my_image.copy()
        draw = ImageDraw.Draw(frame)

        dx, dy = directions[aim]
        start = (center_x + dx * ship_radius, center_y + dy * ship_radius)
        end = (center_x + dx * 30, center_y + dy * 30)
        draw.line((start, end), fill="yellow", width=3)

        if laser is not None:
            laser_direction, laser_color = laser
            dx, dy = directions[laser_direction]
            laser_start = (
                center_x + dx * ship_radius,
                center_y + dy * ship_radius,
            )
            draw.line(
                (laser_start, screen_edges[laser_direction]),
                fill=laser_color,
                width=5,
            )

        for enemy_type, enemy_box in enemy_state:
            color = laser_colors[enemy_type]
            if enemy_type == "A":
                draw.ellipse(enemy_box, fill=color)
            else:
                draw.rectangle(enemy_box, fill=color)
        
        joystick.disp.image(frame)
        last_drawn_state = screen_state

    previous = pressed
    time.sleep(0.02)