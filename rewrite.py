import pygame, os, math
pygame.init()


rows, columns = 16, 16
sizeOfTiles = 16
window = pygame.display.set_mode((rows * sizeOfTiles, columns * sizeOfTiles))
sprites = {}
grid = {}
run = True
mouseX, mouseY = pygame.mouse.get_pos()
#Sprites
darken = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
darken.fill((0, 0, 0, 0.25*255))
darken.convert_alpha()
#Tile Class
class tile:
    def __init__(self, location: tuple, tileValue, tileSprite, gridList, surface,tileSize=16):
        self.tileValue = tileValue
        self.tileSprite = tileSprite
        self.rect = self.tileSprite.get_rect()
        self.gridList = gridList
        self.surface = surface
        self.tileSize = tileSize
        self.isShown = False
        self.shouldUpdate = True
        if len(location) > 2:
            raise Exception("Location tuple in tile class only accepts 2 values")
        elif len(location) < 2:
            raise Exception("Location tuple in tile class requires 2 values")
        else:
            self.row, self.column = location
            self.rect.x = self.row * self.tileSize
            self.rect.y = self.column * self.tileSize
        self.neighbors = {
            "N": f'{self.row} {self.column - 1}',
            "E": f'{self.row + 1} {self.column}',
            "S": f'{self.row} {self.column + 1}',
            "W": f'{self.row - 1} {self.column}',

            "NE": f'{self.row + 1} {self.column - 1}',
            "SE": f'{self.row + 1} {self.column + 1}',
            "NW": f'{self.row - 1} {self.column - 1}',
            "SW": f'{self.row - 1} {self.column + 1}'
        }
    def update(self):
            if self.shouldUpdate == True:
                self.surface.blit(self.tileSprite, (self.rect.x, self.rect.y))
                self.shouldUpdate = False
            if pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()):
                self.surface.blit(darken, (self.rect.x, self.rect.y))
                self.shouldUpdate = True        
    def click(self):
        if pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()):
            if(self.isShown == False):
                self.tileSprite = sprites[self.tileValue]
                self.isShown = True
                self.shouldUpdate = True


def getSprite(path: str, name: str, width: int, height:int , extension: str ="png"):
    getFile = pygame.image.load(path + "/" + name + "." + extension)
    createSurface = pygame.Surface((width, height)).convert_alpha()
    createSurface.blit(getFile, (0, 0))
    return createSurface

def grabSprites():
    spritesList = []
    for directory, what, items in os.walk("sprites/", topdown=False):
        for index in items:
            imgName = str.removesuffix(index, ".png")
            spritesList.append(imgName)
    return(spritesList)
def loadSprites():
    list = grabSprites()
    for i in range(list.__len__()):
        keyValue = getSprite("sprites/", list[i], 16, 16)
        keyName = list[i]
        sprites[keyName] = keyValue

loadSprites()

def createGrid():

    for r in range(rows):
        for c in range(columns):
            tileName = f'{r} {c}'
            tempTile = tile((r, c), "flagTile", sprites["blankTile"], grid, window)
            tempTile.update()
            grid[tileName] = tempTile
createGrid()
def assignMines():
    pass
def click():
    for i in grid:
        grid[i].click()
def tick():
    for i in grid:
        grid[i].update()
while run:
    pygame.time.Clock().tick(60)
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click()
    tick()
    pygame.display.update()