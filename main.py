import pygame
from sys import exit

FPS = 60

colors = {
    "BG" : "#35a5e9"
}

pygame.init()

main_screen = pygame.display.set_mode([640,360])
render_surf = pygame.Surface([320,180])


def Exit_Game():
    print("Yo! this shi be working fine for now")
    pygame.quit()
    exit()

clock = pygame.time.Clock()

while True:
    delta = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit_Game()
    
    render_surf.fill(colors["BG"])
    
    main_screen.blit(pygame.transform.scale_by(render_surf,main_screen.height/render_surf.height),(0,0))
    pygame.display.update()