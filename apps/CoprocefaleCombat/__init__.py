import asyncio
import time

import pygame
import random
import libraries
import requests


libraries.resource_path('resources/audio/KeypressDelete.ogg')


pygame.init()

x, y = 300, 500
FPS = 60
STATUS = ''


async def sync():
    print('Syncing...')
    global coins_buff
    try:
        result = requests.get('http://127.0.0.1:5000/cc/sync', {'user': 'admin', 'coins': coins_buff})
        if result.text == 'OK':
            coins_buff = 0
    except requests.exceptions.ConnectionError:
        pass
    print('Complete!')


def auth():
    pass


class TextPrticle:
    def __init__(self, text, x, y):
        self.surface = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.x, self.y = x, y
        self.vx, self.vy = random.uniform(-0.1, 0.1), -10
        self.text = text


    def move(self):
        self.vy += 0.04 * delta
        self.x += self.vx * delta
        self.y += self.vy

    def render(self):
        pygame.draw.circle(self.surface, '#FFF000', (30, 30), 30)
        pygame.draw.circle(self.surface, '#FF0000', (30, 30), 30, width=3)
        text = font.render(self.text, 1, '#000000')
        self.surface.blit(text, (30 - text.get_size()[0] / 2, 30 - text.get_size()[1] / 2))
        return self.surface


class Button:
    x, y = 210, 210
    actual_radius = 0
    target_radius_pressed = 80
    target_radius_overlayed = 95
    target_radius_unpressed = 100
    result = pygame.Surface((x, y), pygame.SRCALPHA, 32)
    state = 0
    mouse_button = 'UP'

    def check_if_hovering(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if (x/2 - self.x / 2 < mouseX < x/2 + self.x / 2 and
                y/3 - self.y / 2 < mouseY < y/3 + self.y / 2):
            return True
        else:
            return False

    def update(self):
        match self.state:
            case 0:
                self.actual_radius = pygame.math.lerp(self.actual_radius, self.target_radius_unpressed, 0.1)
            case 1:
                self.actual_radius = pygame.math.lerp(self.actual_radius, self.target_radius_overlayed, 0.3)
            case 2:
                self.actual_radius = pygame.math.lerp(self.actual_radius, self.target_radius_pressed, 0.5)


    def render(self):
        self.result.fill((0, 0, 0, 0))
        pygame.draw.circle(self.result, '#f0f0f0', (self.x/2, self.y/2), self.actual_radius)
        return self.result

    def click(self):
        global coins, coins_buff
        coins += 1
        coins_buff += 1
        particles.append(TextPrticle('+1',
                         random.uniform(x/2 - self.actual_radius, x/2 + self.actual_radius),
                         random.uniform(y/3 - self.actual_radius, y/3 + self.actual_radius)))


screen = pygame.display.set_mode((x, y), vsync=True)
pygame.display.set_caption('Coprocefale Combat')
font = pygame.font.SysFont('Arial', 20)
particles: list[TextPrticle] = []
clocks = pygame.time.Clock()

button = Button()
delta = 0
coins = 0
coins_buff = 0
running = True

def main():
    game()


def game():
    timer = 0
    global running
    while running:
        screen.fill('#696969')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if button.check_if_hovering():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button.state = 2
                    button.click()
                elif event.type == pygame.MOUSEBUTTONUP:
                    button.state = 0
                else:
                    button.state = 1
            else:
                button.state = 0

            # if button.check_if_overlayed():
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         button.mouse_button = 'DOWN'
            #         button.click()
            # else:
            #     if event.type == pygame.MOUSEBUTTONUP:
            #         button.mouse_button = 'UP'
        global delta
        delta = clocks.tick(FPS)
        timer += delta

        if timer >= 5000:
            libraries.old_print('TIME!')
            asyncio.run(sync())
            timer = 0

        button.update()
        screen.blit(button.render(), (x/2 - button.x / 2, y/3 - button.y / 2))
        for particle in particles:
            particle.move()
            screen.blit(particle.render(), (particle.x, particle.y))
        screen.blit(font.render(f'{coins} ({coins_buff})', 1, '#FFFFFF'), (0, 0))

        pygame.display.flip()


if __name__ == '__main__':
    main()