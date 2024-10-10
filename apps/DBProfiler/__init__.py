from libraries import *
import requests


def main():
    running = True
    clear_screen('40')
    while running:
        user_input = input('? ').split(' ')
        match user_input:
            case ['help']:
                print('Request example: <key> <password>\n Password isn\'t necessary.')
            case ['exit']:
                running = False
            case ['']:
                pass
            case _:
                key = user_input[0]
                password = user_input[1] if len(user_input) > 1 else None
                Sounds.NetStart.play()
                try:
                    if password:
                        response = requests.get('http://127.0.0.1:5000/',
                                                {'key': key,
                                                 'language': settings['language'],
                                                 'password': password})
                    else:
                        response = requests.get('http://127.0.0.1:5000/get_knowledge',
                                                {'key': key,
                                                 'language': settings['language']})
                except requests.exceptions.ConnectionError:
                    Sounds.NetError.play()
                    print('CAN NOT FETCH')
                    continue
                Sounds.NetComplete.play()
                print(f'{key}:\n{response.json()["response"]}',
                      duration=len(response.json()["response"])/70 if response.json()["response"] else 3)
    clear_screen()