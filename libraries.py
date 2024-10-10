import json
import pygame
import time
import numpy as np
import os
import sys

pygame.init()


def resource_path(filename):
    try:
        open(f'{filename}')
        return f'{filename}'
    except FileNotFoundError:
        try:
            open(f'../{filename}')
            return f'../{filename}'
        except FileNotFoundError:
            open(f'../../{filename}')
            return f'../../{filename}'


class Sounds:
    KeypressDelete = pygame.mixer.Sound(resource_path('resources/audio/KeypressDelete.ogg'))
    KeypressStandard = pygame.mixer.Sound(resource_path('resources/audio/KeypressStandard.ogg'))

    Output = pygame.mixer.Sound(resource_path('resources/audio/Output.ogg'))
    Newline = pygame.mixer.Sound(resource_path('resources/audio/OutputNewline.ogg'))

    NetStart = pygame.mixer.Sound(resource_path('resources/audio/NetInitiated.ogg'))
    NetComplete = pygame.mixer.Sound(resource_path('resources/audio/NetComplete.ogg'))
    NetError = pygame.mixer.Sound(resource_path('resources/audio/NetError.ogg'))

    ErrorCritical = pygame.mixer.Sound(resource_path('resources/audio/Critical.ogg'))


with open(resource_path('settings.json'), 'r') as f:
    settings = json.load(f)


def clear_screen(color='60'):
    if 'linux' in sys.platform:
        print('Linux is not allowed. only windows.')
        quit()
        # os.system('clear')
    elif 'win' in sys.platform:
        os.system('cls')
        os.system(f'color {color}')


old_print = print

def print(text: str, sep=' ', end='\n', duration: int | float = 1):
    modifier = settings["speed_modifier"]
    text = str(text)
    text += end
    last_was_nl = False
    for i in text:
        if i == '\n':
            if not last_was_nl:
                Sounds.Newline.play()
            last_was_nl = True
        else:
            last_was_nl = False
        if i != ' ':
            Sounds.Output.play()
        old_print(i, end='', flush=True)
        time.sleep(duration * modifier / len(text))


def print_number(number: int | float, end='\n', duration: int | float = 1):
    sound = pygame.mixer.Sound('resources/audio/Effect_Tick.ogg')
    end_sound = pygame.mixer.Sound('resources/audio/OutputNewline.ogg')
    if number > 700:
        my_range = 700
        diff = number - 700
        arang = np.arange(700)
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


if __name__ == '__main__':
    pass
else:
    print('libs_init', duration=0.1)