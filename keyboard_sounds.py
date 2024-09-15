import keyboard
import pygame

def main():
    pygame.init()

    standard = pygame.mixer.Sound('resources/audio/KeypressStandard.ogg')
    spacebar = pygame.mixer.Sound('resources/audio/KeypressSpacebar.ogg')
    backspace = pygame.mixer.Sound('resources/audio/KeypressReturn.ogg')
    delete = pygame.mixer.Sound('resources/audio/KeypressDelete.ogg')
    invalid = pygame.mixer.Sound('resources/audio/KeypressInvalid.ogg')
    release = pygame.mixer.Sound('resources/audio/Effect_Tick.ogg')
    enter = pygame.mixer.Sound('resources/audio/KeypressEnter.ogg')

    press_channel = pygame.mixer.Channel(1)

    able = True
    last = ''
    while True:  # infinite loop
        event = keyboard.read_event()
        if event.event_type == 'down':
            if event.name != last:
                if not able:
                    invalid.play()
                    last = event.name
                    continue
                match event.name:
                    case 'space':
                        press_channel.play(spacebar)
                    case 'backspace':
                        press_channel.play(backspace)
                    case 'ctrl' | 'alt' | 'right alt' | 'shift' | 'right shift' | 'tab':
                        press_channel.play(standard)
                    case 'enter':
                        press_channel.play(enter)
                    case _:
                        press_channel.play(delete)
            last = event.name
        if event.event_type == 'up':
            if not press_channel.get_busy():
                release.play()
            last = ''


if __name__ == '__main__':
    print('Keyboard Sounds launched directly!')
    main()
