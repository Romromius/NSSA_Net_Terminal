while True:
    try:
        import json
        import os
        import subprocess
        import sys
        import time
        import pygame
        import keyboard_sounds
        import threading
        break
    except ModuleNotFoundError:
        print('There\'s a problem with libraries.')
        import os
        os.system('fix_dependencies.bat')


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
    last_was_nl = False
    for i in text:
        if i == '\n':
            if not last_was_nl:
                Newline.play()
            last_was_nl = True
        else:
            last_was_nl = False
        if i != ' ':
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
        _ = subprocess.run(["git", "fetch"], check=True)
        status = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True)
    except subprocess.CalledProcessError:
        NetError.play()
        return False

    NetComplete.play()
    if "Your branch is behind" in status.stdout:
        return True
    return False


def pull_updates():
    NetStart.play()
    try:
        subprocess.run(["git", "pull"], check=True)
    except subprocess.CalledProcessError:
        NetError.play()
        my_print('Error while updating.')
        return
    NetComplete.play()


class Commands:
    def __init__(self):
        self.has_updates = None

    def help(self, command):
        with open('help.json', 'r') as f:
            help_info: dict = json.load(f)
            if command:
                if command not in help_info:
                    my_print('There is no info about this command.')
                    return
                my_print(command + ':')
                for i in help_info[command]:
                    my_print('    ' + i)
            else:
                my_print('Type "help <command>" to get help for command.')
                my_print('Arguments in "<>" are meant to be filled with some value.')
                my_print('Arguments that begins with "-" are flags to be just wrote as is.')
                my_print('Available commands:', duration=.5)
                for i in help_info:
                    my_print(' - ' + i, duration=.3)

    def info(self):
        my_print('Displaying system information...')
        my_print('Platform', end='', duration=.5)
        my_print('. ' * 5, end='', duration=3)
        my_print(sys.platform, duration=2)
        my_print('Py version', end='', duration=.5)
        my_print('. ' * 5, end='', duration=3)
        my_print(sys.version, duration=2)
        my_print('Copyrights:\n')
        my_print(sys.copyright, duration=5)

    def update(self, *args: list[str]):
        if args:
            if 'check' in args:
                self.has_updates = check_for_updates()
                if self.has_updates:
                    my_print('New version is available!')
                    pygame.mixer.Sound('resources/audio/Attention.ogg').play(3)
                else:
                    my_print('No updates found.')
            if 'install' in args:
                if self.has_updates is not None:
                    if self.has_updates:
                        pull_updates()
                    else:
                        my_print('There is no updates to install.')
                        my_print('If you sure there are, try checking for updates again.')
                else:
                    my_print('Please first check for updates.')
        else:
            my_print('Please enter arguments.')


background_thread = threading.Thread(target=keyboard_sounds.main, daemon=True)

if __name__ == "__main__":
    background_thread.start()
    clear_screen()
    running = True
    my_print('Hello, NSSA!')
    my_print('Glory to the Watermelon!')
    client = Commands()
    while running:
        user_input = input('> ').split(' ')
        match user_input:

            case ['help', command] | ['help', *command]:
                if command:
                    client.help(command)
                else:
                    client.help(None)
            case ['info']:
                client.info()
            case ['update', *args]:
                client.update(*args)
            case ['exit']:
                my_print('Shutting down...')
                time.sleep(1)
                quit()
            case ['']:
                pass
            case _:
                my_print('Unknown command or wrong arguments.')
                my_print(user_input[0] + ' <-')
