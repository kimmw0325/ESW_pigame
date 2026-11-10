from PIL import Image, ImageDraw, ImageFont
import time
import random
from colorsys import hsv_to_rgb

#from Character import Character
from Joystick import Joystick

joystick = Joystick()

my_image = Image.new("RGB", (joystick.width, joystick.height))
my_draw = ImageDraw.Draw(my_image)
my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 0, 0, 100))
my_draw.text((8, 8), "TOP LEFT", fill = "white")

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
while True:
    pressed = [name for name, button in buttons.items() if not button.value]
    if pressed != previous:
        print(" + ".join(pressed) if pressed else "RELEASED")
        previous = pressed
    time.sleep(0.02)