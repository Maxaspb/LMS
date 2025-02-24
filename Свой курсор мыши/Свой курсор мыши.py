import pygame
import os
 
 
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    return image

 
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Свой курсор мыши')
    all_sprites = pygame.sprite.Group()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites = pygame.sprite.Group()
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            arrow = pygame.sprite.Sprite()
            arrow.image = load_image('arrow.png')
            arrow.rect = arrow.image.get_rect()
            arrow.rect.x = pos[0]
            arrow.rect.y = pos[1]
            all_sprites.add(arrow)
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
