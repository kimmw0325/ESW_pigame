from PIL import Image, ImageDraw, ImageFont
import time
import random
from colorsys import hsv_to_rgb

#from Character import Character
from Joystick import Joystick

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

ship_radius = 12
my_draw.ellipse(
    (center_x - ship_radius, center_y - ship_radius, center_x + ship_radius, center_y + ship_radius),
    fill = "white"
)

joystick.disp.image(my_image)

print("LCD size:", my_image.size)

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

aim = "UP"
previous = []
laser = None
laser_ends_at = 0
last_drawn_state = None

while True:
    pressed = [name for name, button in buttons.items() if not button.value]
    now = time.monotonic()

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

    screen_state = (aim, laser)

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

        joystick.disp.image(frame)
        last_drawn_state = screen_state

    previous = pressed
    time.sleep(0.02)