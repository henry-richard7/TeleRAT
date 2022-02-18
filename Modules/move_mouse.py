import random
import autopy


def move_mouse():
    autopy.mouse.smooth_move(random.randrange(1, 500), random.randrange(1, 500))
