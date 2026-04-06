import pygame
from sys import exit
import random
import yaml

colors = {
    "BG" : "#19c0e6"
}

pygame.init()

main_screen = pygame.display.set_mode([800,800])
render_surf = pygame.Surface([400,400])

class Room():
    def __init__(self,image_path,sockets_path,tilesize,room_size):
        self.grid = {}
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image_set = []
        self.sockets = {}
        self.tiles = {}

        self.size = room_size
        self.tilesize = tilesize

        with open(sockets_path, "r") as file:
            self.sockets = yaml.safe_load(file)
    
    def generate_tile_image(self):
        self.image_set= []
        for y in range(0,self.image.height,self.tilesize):
            for x in random(0,self.image.width,self.tilesize):
                self.imageset.append(self.image.subsurface((x,y),(x+self.tilesize,y+self.tilesize)))

    def generate_grid(self):
        for y in self.size[1]:
            for x in self.size[0]:
                self.grid[(x,y)] = {
                    "collapsed" : False,
                    "candidates" : self.sockets.keys(),
                    "image" : None
                }
    
    def get_min_entropy(self):
        min_entropy = min([len(x["candidates"]) for x in self.grid.values()])

        low_entropy_cells = []

        for cell in self.grid:
            if len(cell["candidates"]) == min_entropy and not cell["collapsed"]:
                low_entropy_cells.append(cell)
        
        if low_entropy_cells == []:
            return
        
        return random.choice(low_entropy_cells)
    
    def collapse_cell(self,cell):
        if cell in self.grid:
            self.grid[cell]["collapsed"] = True
            self.grid[cell]["candidates"] = random.choice(self.sockets.keys())
            self.grid[cell]["Socket"] = 
            }

if __name__ == "__main__":

    def Exit_Game():
        pygame.quit()
        exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit_Game()
        
        render_surf.fill(colors["BG"])
        
        main_screen.blit(pygame.transform.scale_by(render_surf,main_screen.height/render_surf.height),(0,0))
        pygame.display.update()