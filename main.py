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
        import numpy as np
        import datetime
        from datetime import timedelta
        import requests

        from libraries import *
        from apps import *

        break
    except ModuleNotFoundError as err:
        print(f'There\'s a problem with libraries: {err}')
        import os
        os.system('install_requirements.bat')

def check_for_updates():
    Sounds.NetStart.play()

    try:
        _ = subprocess.run(["git", "fetch"], check=True)
        status = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True)
    except subprocess.CalledProcessError:
        Sounds.NetError.play()
        return False

    Sounds.NetComplete.play()
    if "Your branch is behind" in status.stdout:
        return True
    return False


def pull_updates():
    Sounds.NetStart.play()
    try:
        subprocess.run(["git", "pull"], check=True)
    except subprocess.CalledProcessError:
        Sounds.NetError.play()
        print(lang['update_error'])
        return
    Sounds.NetComplete.play()


class UniversalTimeScale:
    def __init__(self):
        # Store time as seconds since year 0
        self.seconds = 0

    # Constants for Earth and Mars time calculations
    SECONDS_IN_DAY = 24 * 60 * 60
    SECONDS_IN_COMMON_YEAR = 365 * SECONDS_IN_DAY
    SECONDS_IN_LEAP_YEAR = 366 * SECONDS_IN_DAY
    SECONDS_IN_MARS_YEAR = 687 * SECONDS_IN_DAY  # Mars year length in seconds

    # Check if a given year is a leap year (for Earth)
    def is_leap_year(self, year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    # Setter to set time by Earth Time Scale (ETS)
    def set_time_by_ets(self, year, add_day_seconds = False):
        total_seconds = 0
        for current_year in range(0, int(year)):
            Sounds.KeypressDelete.play()
            print(total_seconds, end='\r', flush=True)
            if self.is_leap_year(current_year):
                total_seconds += UniversalTimeScale.SECONDS_IN_LEAP_YEAR
            else:
                total_seconds += UniversalTimeScale.SECONDS_IN_COMMON_YEAR
        if add_day_seconds:
            b = datetime.datetime.now()
            b = b.replace(year=1)
            a = 0
            a += b.month * 30 * 24 * 60 * 60
            a += b.day * 24 * 60 * 60
            a += b.hour * 60 * 60
            a += b.minute * 60
            a += b.second
            total_seconds += a
        self.seconds = total_seconds + (year - int(year)) * (UniversalTimeScale.SECONDS_IN_LEAP_YEAR if self.is_leap_year(int(year)) else UniversalTimeScale.SECONDS_IN_COMMON_YEAR)

    # Setter to set time by Martian Time Scale (MTS)
    def set_time_by_mts(self, years):
        self.seconds = years * UniversalTimeScale.SECONDS_IN_MARS_YEAR

    # Getter to get the number of years in Earth Time Scale (ETS), accounting for leap years
    def get_ets_year(self):
        total_seconds = self.seconds
        current_year = 0

        while total_seconds > (UniversalTimeScale.SECONDS_IN_LEAP_YEAR if self.is_leap_year(current_year) else UniversalTimeScale.SECONDS_IN_COMMON_YEAR):
            if self.is_leap_year(current_year):
                total_seconds -= UniversalTimeScale.SECONDS_IN_LEAP_YEAR
            else:
                total_seconds -= UniversalTimeScale.SECONDS_IN_COMMON_YEAR
            current_year += 1

        # Calculate the fractional part of the current year
        if self.is_leap_year(current_year):
            fraction_of_year = total_seconds / UniversalTimeScale.SECONDS_IN_LEAP_YEAR
        else:
            fraction_of_year = total_seconds / UniversalTimeScale.SECONDS_IN_COMMON_YEAR

        return current_year + fraction_of_year

    # Getter to get the number of years in Martian Time Scale (MTS)
    def get_mts_year(self):
        return self.seconds / UniversalTimeScale.SECONDS_IN_MARS_YEAR


class Commands:
    def __init__(self):
        self.has_updates = None

    def help(self, command):
        with open('help.json', 'r') as f:
            help_info: dict = json.load(f)
            if command:
                if command not in help_info:
                    print('')
                    return
                print(command + ':')
                for i in help_info[command]:
                    print('    ' + i)
            else:
                print(lang['help_guide'])
                print(lang['help_available'], duration=.5)
                for i in help_info:
                    print(' - ' + i, duration=.3)

    def info(self):
        print('')
        print(lang['info_platform'], end='', duration=.5)
        print('. ' * 5, end='', duration=3)
        print(sys.platform, duration=2)
        print(lang['info_py_version'], end='', duration=.5)
        print('. ' * 5, end='', duration=3)
        print(sys.version, duration=2)
        print(f'{lang['info_copyrights']}\n')
        print(sys.copyright, duration=5)

    def apps(self):
        print(lang['apps'])
        apps_dir = os.listdir('apps')
        for i in apps_dir:
            if '__init__.py' in os.listdir(f'apps/{i}'):
                print(i)

    def update(self, *args: list[str]):
        if args:
            if '-check' in args:
                self.has_updates = check_for_updates()
                if self.has_updates:
                    print(lang['update_new_ver_available'])
                    # pygame.mixer.Sound('resources/audio/Attention.ogg').play()
                else:
                    print(lang['update_not_found'])
            if '-install' in args:
                if self.has_updates is not None:
                    if self.has_updates:
                        pull_updates()
                    else:
                        print(lang['update_not_remember'])
                else:
                    print(lang['update_ask_to_check'])
        else:
            print(lang['update_ask_argument'])

    def year(self, *args: list[str]):
        year = UniversalTimeScale()
        print('Calculating...')
        year.set_time_by_ets(datetime.datetime.now().year + 12700, add_day_seconds=True)
        if not args or True:
            print(lang['year_uts'], end='')
            print_number(year.seconds, duration=1)
        if '-ets' in args:
            print(lang['year_ets'], end='')
            print_number(year.get_ets_year(), duration=3)
        if '-mts' in args:
            print(lang['year_mts'], end='')
            print_number(year.get_mts_year(), duration=3)


class Language:
    def __init__(self):
        self.language = settings['language']
        print(f'Loading language "{self.language}"')

        self.languages: dict[str, dict] = {'enga': self._dictify('''
greet=Hello, NSSA! Glory to the Watermelon!;
lang_load_success=Language loaded successfully!;
shutdown=Exiting...;
unknown_command=Unknown command or wrong arguments.;
apps=Available apps:;
;
help_no_info=There is no info about this command.;
help_guide=Type "help <command>" to get help for command.
Arguments in "<>" are meant to be filled with some value.
Arguments that begins with "-" are flags to be just wrote as is.;
help_available=Available commands:;
;
info_platform=Platform;
info_py_version=Engine version;
info_copyrights=Copyrights:;
;
update_new_ver_available=New version is available!;
update_not_found=No updates found.;
update_not_remember=There is no updates to install.
If you sure there are, try checking for updates again.;
update_ask_to_check=Please first check for updates.;
update_ask_argument=Please enter arguments.;
update_error=Error while updating.;
;
year_uts=Current UTS value: ;
year_ets=Current ETS year is: ;
year_mts=Current MTS year is: '''),

'russovskoy': self._dictify('''
greet=Привет, НССА! Слава Арбузу!;
lang_load_success=Язык успешно загружен!;
shutdown=Завершение сеанса...;
unknown_command=Неизвестная команда или неверные аргументы.;
apps=Доступные приложения:;
;
help_no_info=О данной команде нет информации.;
help_guide=Используйте "help <command>" чтобы получить помощь по конкретной команде.
Аргументы, заключенные в "<>" должны быть заменены каким-то значением.
Аргументы, начинающиеся с "-" являются флагами и должны быть указаны как есть.;
help_available=Доступные команды:;
;
info_platform=Платформа;
info_py_version=Версия движка;
info_copyrights=Правовая информация:;
;
update_new_ver_available=Доступна новая версия!;
update_not_found=Обновления не найдены.;
update_not_remember=Нет обновлений, доступных для установки.
Если вы уверены, что есть, попробуйте проверить наличие обновлений.;
update_ask_to_check=Пожалуйста, сначала проверьте наличие обновлений.;
update_ask_argument=Укажите аргументы.;
update_error=Во время обновления произошла ошибка.;
;
year_uts=Значение UTS: ;
year_ets=Год по ETS: ;
year_mts=Год по MTS: ''')
                                           }

        if not self.languages.get(self.language, False):
            self.language = 'english'
            pygame.mixer.Sound('resources/audio/Error.ogg').play()
            print('Failed to load this language!')
        else:
            print(self.__repr__()['lang_load_success'])


    def _dictify(self, string: str) -> dict:
        result = {}
        for i in string.split(';'):
            try:
                result[i.split('=')[0][1:]] = i.split('=')[1]
            except IndexError:
                continue
        return result

    def __repr__(self) -> dict:
        return self.languages[self.language]

    def __getitem__(self, item):
        string = self.languages[self.language].get(item, False)
        if string:
            return string
        else:
            pygame.mixer.Sound('resources/audio/Trouble.ogg').play()
            return f'LOCALISATION ERROR: {item} NOT FOUND'


background_thread = threading.Thread(target=keyboard_sounds.main, daemon=True)

if __name__ == "__main__":
    background_thread.start()
    clear_screen()
    running = True
    lang = Language()
    print(lang['greet'])
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
            case ['apps']:
                client.apps()
            case ['update', *args]:
                client.update(*args)
            case ['exit']:
                print(lang['shutdown'])
                time.sleep(1)
                running = False
            case ['year', *args]:
                client.year(*args)
            case ['']:
                pass
            case _:
                try:
                    if '__init__.py' in os.listdir(f'apps/{user_input[0]}'):
                        exec(f'from apps import {user_input[0]}\n'
                             f'{user_input[0]}.main()')

                        continue
                except ModuleNotFoundError:
                    pass
                except AttributeError as err:
                    Sounds.ErrorCritical.play()
                    print(f'Error in {user_input[0]}: {err}')  # TODO: Перевести
                    continue

                print(lang['unknown_command'])
                print(user_input[0] + ' <-')
    clear_screen('F0')
