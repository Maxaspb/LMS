import pygame
import os

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image

class Car(pygame.sprite.Sprite):
    def __init__(self, im, x, y, all_sprites):
        super().__init__(all_sprites)
        self.image = load_image(im)
        self.rect = self.image.get_rect()
        self.x = float(x)
        self.y = float(y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 95))
    pygame.display.set_caption('Машинка')
    all_sprites = pygame.sprite.Group()
    car = Car('car2.png', 0, 0, all_sprites)
    delta = 1
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        new_x = car.x + delta
        if new_x < 0:
            delta = abs(delta)
            car.image = pygame.transform.flip(car.image, True, False)
            car.x = 0
        elif new_x + car.rect.width > 600:
            delta = -abs(delta)
            car.image = pygame.transform.flip(car.image, True, False)
            car.x = 600 - car.rect.width
        else:
            car.x = new_x
        car.rect.x = int(car.x)
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
