import json
import os
import subprocess
import sys
import time
import pygame
import keyboard_sounds
import threading


pygame.init()
KeypressDelete = pygame.mixer.Sound('resources/audio/KeypressDelete.ogg')
KeypressStandard = pygame.mixer.Sound('resources/audio/KeypressStandard.ogg')

Output = pygame.mixer.Sound('resources/audio/Output.ogg')
Newline = pygame.mixer.Sound('resources/audio/OutputNewline.ogg')

NetStart = pygame.mixer.Sound('resources/audio/NetInitiated.ogg')
NetComplete = pygame.mixer.Sound('resources/audio/NetComplete.ogg')
NetError = pygame.mixer.Sound('resources/audio/NetError.ogg')


def my_print(text: str, sep=' ', end='\n', duration: int | float = 1):
    modifier = 1
    text += end
    for i in text:
        if i == '\n':
            Newline.play()
        elif i != ' ':
            Output.play()
        print(i, end='', flush=True)
        time.sleep(duration * modifier / len(text))



def clear_screen():
    if 'linux' in sys.platform:
        os.system('clear')
    elif 'win' in sys.platform:
        os.system('cls')


def check_for_updates():
    NetStart.play()

    try:
        subprocess.run(["git", "fetch"], check=True)
        status = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True)
    except subprocess.CalledProcessError:
        NetError.play()
        return False

    NetComplete.play()
    if "Your branch is behind" in status.stdout:
        return True
    return False


def pull_updates():
    # Pull updates from remote repository
    subprocess.run(["git", "pull"], check=True)


background_thread = threading.Thread(target=keyboard_sounds.main, daemon=True)

if __name__ == "__main__":
    background_thread.start()
    print('RUNUNGI')
    clear_screen()
    running = True
    my_print('Hello, NSSA!')
    my_print('Glory to the Watermelon!')
    while running:
        user_input = input('> ').split(' ')
        match user_input:

            case ['help', *command]:
                with open('help.json', 'r') as f:
                    help_info: dict = json.load(f)
                    if command:
                        if command[0] not in help_info:
                            my_print('There is no info about this command.')
                            continue
                        my_print(command[0] + ':')
                        for i in help_info[command[0]]:
                            my_print('    ' + i)
                    else:
                        my_print('Type "help <command>" to get help for command.')
                        my_print('Available commands:')
                        for i in help_info:
                            my_print(' - ' + i)
            case ['info']:
                my_print('Displaying system information...')
                my_print('Platform', end='', duration=.5)
                my_print('. ' * 5, end='', duration=3)
                my_print(sys.platform, duration=2)
                my_print('Py version', end='', duration=.5)
                my_print('. ' * 5, end='', duration=3)
                my_print(sys.version, duration=2)
                my_print('Copyrights:\n')
                my_print(sys.copyright, duration=5)
            case ['updates', *args]:
                if args:
                    if 'check' in args:
                        check_for_updates()
                else:
                    my_print('Please enter arguments.')
            case ['']:
                pass
            case _:
                my_print('Unknown command or wrong arguments.')
                my_print(user_input[0] + ' <-')
