import math
import time
from datetime import datetime

import pygame
import numpy as np

from main import my_print

pygame.init()


def print_number(number: int | float, end='\n', duration: int | float = 1):
    sound = pygame.mixer.Sound('resources/audio/Effect_Tick.ogg')
    end_sound = pygame.mixer.Sound('resources/audio/OutputNewline.ogg')
    if number > 100:
        my_range = 100
        diff = number - 100
        arang = np.arange(100)
    else:
        my_range = number
        diff = 0
        arang = np.arange(number)

    for i in range(my_range):
        to_print = int(number / my_range * (i + 1))
        print(to_print, end='', flush=True)
        print('\b' * len(str(to_print)), end='', flush=True)
        lam = .1
        C = 1 / np.sum(np.exp(lam * arang))
        sleep_time = duration / 3 * C * np.exp(lam * i + 1)
        if not pygame.mixer.get_busy():
            sound.play()
        time.sleep(sleep_time)
    end_sound.play()
    print(end=end)


print('The num is: ', end='')
print_number(15000, duration=3)
print_number(15000, duration=1)
print_number(10, duration=10)
time.sleep(1)