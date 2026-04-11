import pygame
from sys import exit
import random
import yaml

colors = {
    "BG" : "#ae6a47"
}

pygame.init()

main_screen = pygame.display.set_mode([1920,1080])
render_surf = pygame.Surface([1920,1080])

mouse_cord_font = pygame.font.SysFont("arial",35)

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,image,size):
        super().__init__()
        self.grid_cell = pos
        self.pos = [p*size for p in pos]
        self.baseimg = image.copy()
        self.image = self.baseimg.copy()
        self.rect = pygame.Rect((self.pos),(size,size))
        tilegroup.add(self)

tilegroup = pygame.sprite.Group()
class Room():
    def __init__(self,image_path,sockets_path,tilesize,room_size):
        self.corners = {}
        self.grid = {}
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image_set = []
        self.sockets = {}
        self.classes = []

        self.size = room_size
        self.tilesize = tilesize

        with open(sockets_path,"r") as file:
            s = yaml.safe_load(file)
            self.classes = s["Classes"]
            self.sockets = {k : v for k,v in s.items() if type(k) is not str}

        for y in range(0,self.image.height - self.tilesize + 1,self.tilesize):
            for x in range(0,self.image.width - self.tilesize + 1,self.tilesize):
                self.image_set.append(self.image.subsurface((x,y),(self.tilesize,self.tilesize)))
        
        self.generate_grid()
        while sum([not cell["collapsed"] for cell in self.grid.values()]):
            self.collapse_cell(self.get_lowest_entropy_cell())

    def get_lowest_entropy_cell(self):
        cells = []
        min_entropy = float("inf")
        for x,y in self.grid:

            if self.grid[(x,y)]["collapsed"]:
                continue

            corners = [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]

            entropy = 0
            for corner in corners:
                entropy += len(self.corners[corner])
            
            if entropy < min_entropy:
                min_entropy = entropy
                cells.clear()
                cells.append((x,y))
            elif entropy == min_entropy:
                cells.append((x,y))
        return random.choice(cells)

    def generate_grid(self):
        for y in range(self.size[1]+1):
            for x in range(self.size[0]+1):
                self.corners[(x,y)] = self.classes.copy()
        
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.grid[(x,y)] = {
                    "collapsed" : False,
                    "tile" : None 
                }

    def collapse_corners(self,corners):
        min_entropy = float("inf")
        candidates = []
        corners_copy = corners.copy()
        while corners_copy:
            for corner in corners_copy:
                entropy = len(self.corners[corner])
                if min_entropy > entropy:
                    min_entropy = entropy
                    candidates.clear()
                    candidates.append(corner)
                elif min_entropy == entropy:
                    candidates.append(corner)
            removed = random.choice(candidates)
            min_entropy = float("inf")
            candidates = []
            corners_copy.remove(removed)
            self.corners[removed] = [random.choice(self.corners[removed])]
            self.propagate_corner(removed)

    def collapse_cell(self,pos:tuple):
        if self.grid[pos]["collapsed"]:
            return

        x,y = pos
        corner_cords = [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]

        self.collapse_corners(corner_cords)
        
        corners = [self.corners[cord][0] for cord in corner_cords]
        candidates = []
        for _id,socket in self.sockets.items():
            if corners == socket:
                candidates.append(_id)
        
        if not candidates:
            candidates = [12]
        self.grid[pos]["tile"] = Tile(pos,self.image_set[random.choice(candidates)],32)
        self.grid[pos]["collapsed"] = True

    def propagate_corner(self,corner):
        neighbours = []
        current_corner = self.corners[corner].copy()      
        if current_corner != [None]:
            current_corner = current_corner*10

        for y in range(corner[1]-1,corner[1]+1):
            for x in range(corner[0]-1,corner[0]+1):
                if (x,y) in self.corners:
                    if len(self.corners[(x,y)]) == 1:
                        continue
                    neighbours.append((x,y))
                
        for cord in neighbours:
            self.corners[cord].extend(current_corner + ["G"]*cord[1]*20)

    def mouse_check(self, mouse_pos):
        tiles = tilegroup.sprites()
        for tile in tiles:
            if tile.rect.collidepoint(mouse_pos):

                
                x,y = (i//32 for i in mouse_pos)
                corners = [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
                if pygame.mouse.get_pressed()[0]:
                    for corner in corners:
                        self.corners[corner] = ["G"]
                elif pygame.mouse.get_pressed()[2]:
                    for corner in corners:
                        self.corners[corner] = [None]
                
                for ty in range(y-1,y+2):
                    for tx in range(x-1,x+2):
                        if (tx,ty) == (x,y) or (tx,ty) not in self.grid:
                            continue
                        
                        if (tx,ty) in self.grid:
                            corners = [(tx,ty),(tx+1,ty),(tx,ty+1),(tx+1,ty+1)]
                            cell_socket = [self.corners[corner][0] for corner in corners]

                        for _id,socket in self.sockets.items():
                            if cell_socket == socket:
                                img = self.image_set[_id]
                                self.grid[(tx,ty)]["tile"].baseimg = img.copy()
                                self.grid[(tx,ty)]["tile"].image = img.copy()
                                break
            else:
                if tile.image != tile.baseimg:
                    tile.image = tile.baseimg.copy()
    
    def update(self,mouse_pos):
        self.mouse_check(mouse_pos)

if __name__ == "__main__":

    def Exit_Game():
        pygame.quit()
        exit()
    
    def draw_highlight(mouse_pos):
        x,y = ((i//32)*32-16 for i in mouse_pos)
        image = pygame.Surface((32,32))
        image.fill("#222222")
        render_surf.blit(image,(x,y),special_flags=pygame.BLEND_RGB_ADD)
    
    room1 = Room("grass-tiles.png","sockets.yaml",32,(render_surf.width//32+1,render_surf.height//32+1))
    grid = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit_Game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                tilegroup.empty()
                room1 = Room("grass-tiles.png","sockets.yaml",32,(render_surf.width//32+1,render_surf.height//32+1))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                grid = not grid
        
        mouse_pos = pygame.mouse.get_pos()
        render_surf.fill(colors["BG"])
        tilegroup.draw(render_surf)
        room1.update(mouse_pos)
        draw_highlight(mouse_pos)
        mouse_cord_text = mouse_cord_font.render(f"Grid Cell: {[x//32 for x in mouse_pos]}",True,"#543344","#8ea091")
        mouse_cord_rect = mouse_cord_text.get_rect(midtop=(render_surf.width//2,0))
        render_surf.blit(mouse_cord_text,mouse_cord_rect)

        if grid:
            for x in range(-16,render_surf.width+16,32):
                pygame.draw.line(render_surf,(0,0,0),(x,0),(x,render_surf.height),1)
            for y in range(-16,render_surf.height+16,32):
                pygame.draw.line(render_surf,(0,0,0),(0,y),(render_surf.width,y),1)
        
        main_screen.blit(pygame.transform.scale_by(render_surf,main_screen.height/render_surf.height),(0,0))

        pygame.display.update()