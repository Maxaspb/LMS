import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image


class Mountain(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.image = load_image('mountains.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = 600
        self.mask = pygame.mask.from_surface(self.image)


class Landing(pygame.sprite.Sprite):
    def __init__(self, pos, all_sprites):
        super().__init__(all_sprites)
        self.image = load_image('pt.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 1)
        
        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((789, 600))
    pygame.display.set_caption('Высадка десанта')
    all_sprites = pygame.sprite.Group()
    mountain = Mountain(all_sprites)
    running = True
    while running:
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                landing = Landing(event.pos, all_sprites)
                if pygame.sprite.collide_mask(landing, mountain):
                    landing.kill()
        pygame.time.delay(20)
    pygame.quit()
