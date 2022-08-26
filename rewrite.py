import pygame, os, random
pygame.init()


rows, columns = 16, 16
amountOfMines = 247
loss = False
sizeOfTiles = 16
window = pygame.display.set_mode((((rows * sizeOfTiles)), ((columns * sizeOfTiles))))
sprites = {}
grid = {}
run = True
assignedMines = False
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
        self.rect = sprites[self.tileSprite].get_rect()
        self.gridList = gridList
        self.surface = surface
        self.tileSize = tileSize
        self.isShown = False
        self.shouldUpdate = True
        self.flagged = False
        self.countLog = ""
        if len(location) > 2:
            raise Exception("Location tuple in tile class only accepts 2 values")
        elif len(location) < 2:
            raise Exception("Location tuple in tile class requires 2 values")
        else:
            self.row, self.column = location
            self.rect.x = self.row * self.tileSize
            self.rect.y = self.column * self.tileSize
        self.neighbors = {
            "N": f"{f'{self.row} {self.column}' if self.column - 1 < 0 else f'{self.row} {self.column - 1}'}",
            "E": f"{f'{self.row} {self.column}' if self.row + 1 > rows - 1 else f'{self.row + 1} {self.column}'}",
            "S": f"{f'{self.row} {self.column}' if self.column + 1 > columns - 1 else f'{self.row} {self.column + 1}'}",
            "W": f"{f'{self.row} {self.column}' if self.row - 1 < 0 else f'{self.row - 1} {self.column}'}",

            "NE": f"{f'{self.row} {self.column}' if self.row + 1 > rows - 1 or self.column - 1 < 0 else f'{self.row + 1} {self.column - 1}'}",
            "SE": f"{f'{self.row} {self.column}' if self.row + 1  > rows - 1 or self.column + 1 > columns - 1 else f'{self.row + 1} {self.column + 1}'}",
            "NW": f"{f'{self.row} {self.column}' if self.row - 1 < 0 or self.column - 1 < 0 else f'{self.row - 1} {self.column - 1}'}",
            "SW": f"{f'{self.row} {self.column}' if self.row - 1 < 0 or self.column + 1 > columns - 1 else f'{self.row - 1} {self.column + 1}'}"
        }
        self.neighboringMines = 0
    def sendMines(self):
        if self.tileValue != "mineTile":
            backlogCount = 0
            if grid[self.neighbors["N"]].tileValue == "mineTile":
                backlogCount = 0
                self.neighboringMines += 1
                backlogCount += 1
                self.countLog += "\nN: " + f'{backlogCount}'
            if grid[self.neighbors["E"]].tileValue == "mineTile":
                backlogCount = 0
                self.neighboringMines += 1
                backlogCount += 1
                self.countLog += "\nE:" + f'{backlogCount}'
            if grid[self.neighbors["S"]].tileValue == "mineTile":
                backlogCount = 0
                self.neighboringMines += 1
                backlogCount += 1
                self.countLog += "\nS: " + f'{backlogCount}'
            if grid[self.neighbors["W"]].tileValue == "mineTile":
                backlogCount = 0
                self.neighboringMines += 1
                backlogCount += 1
                self.countLog += "\nW: "  + f'{backlogCount}'
            if grid[self.neighbors["NE"]].tileValue == "mineTile":
                backlogCount = 0
                self.neighboringMines += 1
                backlogCount += 1
                self.countLog += "\nNE: "  + f'{backlogCount}'
            if grid[self.neighbors["SE"]].tileValue == "mineTile":
                backlogCount = 0
                self.neighboringMines += 1
                backlogCount += 1
                self.countLog += "\nSE: "  + f'{backlogCount}'
            if grid[self.neighbors["SW"]].tileValue == "mineTile":
                backlogCount = 0
                self.neighboringMines += 1
                backlogCount += 1
                self.countLog += "\nSW: "  + f'{backlogCount}'
            if grid[self.neighbors["NW"]].tileValue == "mineTile":
                backlogCount = 0
                self.neighboringMines += 1
                backlogCount += 1
                self.countLog += "\nNW: "  + f'{backlogCount}'
        """if self.tileValue == "mineTile":
            grid[self.neighbors["N"]].neighboringMines += 1
            grid[self.neighbors["E"]].neighboringMines += 1
            grid[self.neighbors["S"]].neighboringMines += 1
            grid[self.neighbors["W"]].neighboringMines += 1
            grid[self.neighbors["NE"]].neighboringMines += 1
            grid[self.neighbors["SE"]].neighboringMines += 1
            grid[self.neighbors["SW"]].neighboringMines += 1
            grid[self.neighbors["NW"]].neighboringMines += 1"""
    def update(self):
            if self.shouldUpdate == True:
                if(self.isShown == True):
                    if(self.tileValue == "blankTile"):
                        if(self.neighboringMines == 0):
                            self.tileSprite = "emptyTile"
                        if(self.neighboringMines == 1):
                            self.tileSprite = "tileOne"
                        if(self.neighboringMines == 2):
                            self.tileSprite = "tileTwo"
                        if(self.neighboringMines == 3):
                            self.tileSprite = "tileThree"
                        if(self.neighboringMines == 4):
                            self.tileSprite = "tileFour"
                        if(self.neighboringMines == 5):
                            self.tileSprite = "tileFive"
                        if(self.neighboringMines == 6):
                            self.tileSprite = "tileSix"
                        if(self.neighboringMines == 7):
                            self.tileSprite = "tileSeven"
                        if(self.neighboringMines == 8):
                            self.tileSprite = "tileEight"
                elif self.flagged == True:
                    self.tileSprite = "flagTile"
                elif self.flagged == False:
                    self.tileSprite = "blankTile"
                self.surface.blit(sprites[self.tileSprite], (self.rect.x, self.rect.y))
                self.shouldUpdate = False
            if pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()):
                self.surface.blit(darken, (self.rect.x, self.rect.y))
                self.shouldUpdate = True        
    def click(self, flag, recurse=False):
        global loss
        if pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()) or recurse == True:
                #print(self.countLog, "\n", self.neighboringMines, "\n", self.neighbors, "\n", self.row, self.column)
                if flag == True:
                    if self.flagged == True:
                        print("A")
                        self.flagged = False
                    else:
                        print("B")
                        self.flagged = True
                    self.shouldUpdate = True
                elif(self.tileValue == "mineTile" and self.flagged == False):
                    
                    for i in grid:
                        if(grid[i].tileValue == "mineTile"):
                            grid[i].tileSprite = grid[i].tileValue
                            grid[i].isShown = True
                            grid[i].shouldUpdate = True
                            loss = True
                elif(self.isShown == False and self.flagged == False):
                    self.tileSprite = self.tileValue
                    self.isShown = True
                    self.shouldUpdate = True
                    if self.neighboringMines == 0:
                        for i in self.neighbors:
                            grid[self.neighbors[i]].click(False, True)


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
def assignMines():
    global assignedMines
    minesLeft = amountOfMines
    while minesLeft > 0:
        changeToMine = random.choice(list(grid))
        if(grid[changeToMine].tileValue != "mineTile"):
            if(pygame.Rect.collidepoint(grid[grid[changeToMine].neighbors["N"]].rect, pygame.mouse.get_pos()) or pygame.Rect.collidepoint(grid[grid[changeToMine].neighbors["E"]].rect, pygame.mouse.get_pos()) or pygame.Rect.collidepoint(grid[grid[changeToMine].neighbors["S"]].rect, pygame.mouse.get_pos()) or pygame.Rect.collidepoint(grid[grid[changeToMine].neighbors["W"]].rect, pygame.mouse.get_pos()) or pygame.Rect.collidepoint(grid[grid[changeToMine].neighbors["NE"]].rect, pygame.mouse.get_pos()) or pygame.Rect.collidepoint(grid[grid[changeToMine].neighbors["NW"]].rect, pygame.mouse.get_pos()) or pygame.Rect.collidepoint(grid[grid[changeToMine].neighbors["SE"]].rect, pygame.mouse.get_pos()) or pygame.Rect.collidepoint(grid[grid[changeToMine].neighbors["SW"]].rect, pygame.mouse.get_pos()) or pygame.Rect.collidepoint(grid[changeToMine].rect, pygame.mouse.get_pos())):
                pass
            else:
                grid[changeToMine].tileValue = "mineTile"
                minesLeft -= 1
    for i in grid:
        grid[i].sendMines()
    print("Mines created")
    assignedMines = True
def createGrid():

    for r in range(rows):
        for c in range(columns):
            tileName = f'{r} {c}'
            tempTile = tile((r, c), "blankTile", "blankTile", grid, window)
            tempTile.update()
            grid[tileName] = tempTile
createGrid()
def click(flag=False):
    if(assignedMines == False and flag == False):
        assignMines()
    for i in grid:
        grid[i].click(flag)
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
            if loss == False:
                if event.button == 1:
                    click()
                if event.button == 3:
                    click(True)
    tick()
    pygame.display.update()