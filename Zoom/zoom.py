import pygame
        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((501, 501))
    pygame.display.set_caption('Zoom')
    file = open('points.txt', encoding='utf8')
    points = [(float(i.split(';')[0][1:].replace(',', '.')), -float(i.split(';')[1][:-1].replace(',', '.'))) for i in file.readlines()[0].split(', ')]
    k = 8
    running = True
    while running:
        screen.fill((0, 0, 0))
        points_now = [(i[0] * k + 250, i[1] * k + 250) for i in points]
        pygame.draw.polygon(screen, 'white', points_now, 1)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 4:
                    k *= 2
                if event.button == 5:
                    k /= 2
    pygame.quit()
