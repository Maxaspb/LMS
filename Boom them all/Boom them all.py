import pygame
import os
from random import randint
 
 
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image


class Bomb(pygame.sprite.Sprite):
    def __init__(self, im, x, y, all_sprites):
        super().__init__(all_sprites)
        self.image = load_image(im)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

 
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Boom them all')
    all_sprites = pygame.sprite.Group()
    for i in range(20):
        x = randint(0, 426)
        y = randint(0, 430)
        bomb = Bomb('bomb.png', x, y, all_sprites)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i in all_sprites:
                    if i.rect.collidepoint(pos):
                        i.image = pygame.transform.scale(load_image('boom.png'), (74, 70))
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
