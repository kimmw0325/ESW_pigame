from PIL import Image, ImageDraw, ImageFont
import time
import random
from pathlib import Path
from colorsys import hsv_to_rgb

#from Character import Character
from Joystick import Joystick
from Enemy import Enemy

joystick = Joystick()

assets_dir = Path(__file__).resolve().parent / "assets"

with Image.open(assets_dir / "background.png") as image:
    my_image = image.convert("RGB")

center_x = joystick.width // 2
center_y = joystick.height // 2
ship_radius = 12
max_health = 3
muzzle_distance = 19


def load_sprite(filename):
    with Image.open(assets_dir / filename) as image:
        return image.convert("RGBA")


def turret_rotations(filename):
    up = load_sprite(filename)
    return {
        "UP": up,
        "RIGHT": up.transpose(Image.Transpose.ROTATE_270),
        "DOWN": up.transpose(Image.Transpose.ROTATE_180),
        "LEFT": up.transpose(Image.Transpose.ROTATE_90),
    }


turrets = {
    False: turret_rotations("turret_up.png"),
    True: turret_rotations("turret_locked_up.png"),
}

enemy_sprites = {
    "A": load_sprite("enemy_a.png"),
    "B": load_sprite("enemy_b.png"),
}

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

laser_colors = {"A": "#FF4855", "B": "#59CCFF"}

screen_edges = {
    "UP":    (center_x, 0),
    "DOWN":  (center_x, joystick.height - 1),
    "LEFT":  (0, center_y),
    "RIGHT": (joystick.width - 1, center_y),
}

start_image = Image.new("RGB", my_image.size)
start_draw = ImageDraw.Draw(start_image)
start_draw.text(
    (center_x, center_y - 15), "SPACE PEWPEW", fill="white", anchor="mm"
)
start_draw.text(
    (center_x, center_y + 15), "PRESS A TO START", fill="white", anchor="mm"
)
joystick.disp.image(start_image)

new_round = True

while True:
    if new_round:
        # A를 누르고 있으면 손을 뗄 때까지 기다린다.
        while not joystick.button_A.value:
            time.sleep(0.02)

        # A를 새로 누르면 한 판을 시작한다.
        while joystick.button_A.value:
            time.sleep(0.02)

        enemies = []
        health = max_health # 체력 개수
        game_started_at = time.monotonic()
        next_spawn_at = game_started_at + 1.2

        aim = "UP"
        previous = ["A"] # 시작할 때 누른 A로 바로 발사되는 걸 막는다.
        laser = None
        laser_ends_at = 0
        next_shot_at = 0
        last_drawn_state = None
        previous_time = game_started_at

        new_round = False

    pressed = [name for name, button in buttons.items() if not button.value]
    now = time.monotonic()

    elapsed = now - previous_time # 경과 시간
    previous_time = now

    for enemy in enemies:
        enemy.distance -= 20 * elapsed # 적 이동속도
        dx, dy = directions[enemy.direction]
        enemy.x = center_x + dx * enemy.distance
        enemy.y = center_y + dy * enemy.distance

    enemy_count_before_contact = len(enemies)
    enemies = [
        enemy for enemy in enemies
        if enemy.distance > ship_radius + enemy.radius
    ]
    damage = enemy_count_before_contact - len(enemies)
    health = max(0, health - damage)

    if health == 0:
        game_over_image = Image.new("RGB", my_image.size)
        game_over_draw = ImageDraw.Draw(game_over_image)

        game_over_draw.text((center_x, center_y - 15), "GAME OVER", fill="white", anchor="mm")
        game_over_draw.text((center_x, center_y + 15), "PRESS A TO RETRY", fill="white", anchor="mm")

        joystick.disp.image(game_over_image)
        new_round = True
        continue

    if now >= next_spawn_at:
        direction = random.choice(list(directions))

        spawn_x, spawn_y = screen_edges[direction]

        distance = abs(spawn_x - center_x) + abs(spawn_y - center_y)

        enemy_type = random.choice(("A", "B"))

        enemies.append(Enemy(spawn_x, spawn_y, direction, distance, enemy_type))

        game_elapsed = now - game_started_at
        difficulty_level = int(game_elapsed // 5)
        spawn_interval = max(0.75, 1.5 - 0.25 * difficulty_level) # 적 스폰 간격(최소 0.75)
        next_spawn_at = now + spawn_interval

    for direction in directions:
        if direction in pressed:
            aim = direction
            break

    for button_name, color in laser_colors.items():
        if (
            button_name in pressed
            and button_name not in previous
            and now >= next_shot_at
        ):
            laser = (aim, color)
            laser_ends_at = now + 0.15

            enemy_count_before = len(enemies)
            enemies = [
                enemy for enemy in enemies
                if not (
                    enemy.direction == aim
                    and enemy.enemy_type == button_name
                )
            ]

            if len(enemies) == enemy_count_before:
                next_shot_at = now + 1

            break

    if laser is not None and now >= laser_ends_at:
        laser = None

    enemy_state = tuple(
        (enemy.enemy_type, tuple(round(value) for value in enemy.bounds()))
        for enemy in enemies
    )

    cooldown_active = now < next_shot_at
    screen_state = (aim, laser, enemy_state, cooldown_active, health)

    if screen_state != last_drawn_state:
        frame = my_image.copy()
        draw = ImageDraw.Draw(frame)

        turret = turrets[cooldown_active][aim]
        frame.paste(
            turret,
            (center_x - turret.width // 2, center_y - turret.height // 2),
            turret,
        )

        if laser is not None:
            laser_direction, laser_color = laser
            dx, dy = directions[laser_direction]
            laser_start = (
                center_x + dx * muzzle_distance,
                center_y + dy * muzzle_distance,
            )
            draw.line(
                (laser_start, screen_edges[laser_direction]),
                fill=laser_color,
                width=5,
            )

        for enemy_type, enemy_box in enemy_state:
            sprite = enemy_sprites[enemy_type]
            frame.paste(sprite, enemy_box[:2], sprite)

        draw.text((8, 8), "HP", fill="white")

        for index in range(max_health):
            x = 28 + index * 16
            color = "#55F2AD" if index < health else "#14263B"
            draw.rectangle(
                (x, 8, x + 11, 17),
                fill=color,
                outline="#41617A",
            )
        joystick.disp.image(frame)
        last_drawn_state = screen_state

    previous = pressed
    time.sleep(0.02)