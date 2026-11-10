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

previous = []
directions = {
    "UP":    (0, -1),
    "DOWN":  (0, 1),
    "LEFT":  (-1, 0),
    "RIGHT": (1, 0),
}

aim = "UP"
prev_aim = None
previous = []

while True:
    pressed = [name for name, button in buttons.items() if not button.value]

    if pressed != previous:
        print(" + ".join(pressed) if pressed else "RELEASED")
        previous = pressed

    for direction in directions:
        if direction in pressed:
            aim = direction
            break

    if aim != prev_aim: 
        frame = my_image.copy()
        draw = ImageDraw.Draw(frame)
        dx, dy = directions[aim]

        start = (center_x + dx * ship_radius, center_y + dy * ship_radius)
        end = (center_x + dx * 30, center_y + dy * 30)
        draw.line((start, end), fill="yellow", width=3)

        joystick.disp.image(frame)
        prev_aim = aim
    time.sleep(0.02)