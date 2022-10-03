import pygame, os, random
pygame.init()


rows, columns = 0, 0
amountOfMines = 40
loss = False
sizeOfTiles = 16
gameScreen = pygame.display.set_mode((400, 400))
gameInitiated = False
sprites = {}
textboxes = {}
grid = {}
run = True
assignedMines = False
mouseX, mouseY = pygame.mouse.get_pos()
#Sprites
darken = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
darken.fill((0, 0, 0, 0.25*255))
darken.convert_alpha()
def getSprite(path: str, name: str,extension: str ="png"):
    getFile = pygame.image.load(path + "/" + name + "." + extension)
    createSurface = pygame.Surface((getFile.get_width(), getFile.get_height())).convert_alpha()
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
        keyValue = getSprite("sprites/", list[i])
        keyName = list[i]
        sprites[keyName] = keyValue

loadSprites()
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
            self.rect.y = (self.column * self.tileSize) + (sizeOfTiles * 2)
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
        self.neighboringFlagged = 0
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
    def countFlagged(self):
        if self.flagged == True:
            for i in self.neighbors:
                grid[self.neighbors[i]].neighboringFlagged += 1
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
    def click(self, flag, recurse=False, surroundingTiles=False):
        global loss, assignedMines
        if pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()) or recurse == True or surroundingTiles == True:
                #print(self.countLog, "\n", self.neighboringMines, "\n", self.neighbors, "\n", self.row, self.column)
                if(self.isShown == True and self.flagged == False and self.neighboringFlagged == self.neighboringMines and assignedMines == True):
                    for i in self.neighbors:
                        if grid[self.neighbors[i]].isShown == False:
                            grid[self.neighbors[i]].click(False, False, True)
                if flag == True:
                    if self.isShown == False:
                        if self.flagged == True:
                            self.flagged = False
                        else:
                            self.flagged = True
                    self.countFlagged()
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
class textBox:
    def __init__(self, position: tuple, size: tuple, fontsize: int or float, label: str):
        self.x, self.y = position
        self.w, self.h = size
        self.labelValue = label
        self.label = 0
        self.font = pygame.font.Font("PressStart-Modified.ttf", fontsize)
        self.textValue = ""
        self.text = 0
        self.sprite = sprites["buttonPressed"]
        self.sprite = pygame.transform.scale(self.sprite, (self.w, self.h))
        textboxes[label] = self
    def draw(self):
        self.text = self.font.render(self.textValue, False, (0, 0, 0))
        self.label = self.font.render(self.labelValue, False, (0, 0, 0))
        gameScreen.blit(self.sprite, (self.x - (self.w/2), self.y - (self.h/2)))
        gameScreen.blit(self.text, (self.x - (self.w/2), self.y - (self.h/2)))
        gameScreen.blit(self.label, (self.x - (self.w / 2), self.y - ((self.h / 2) + self.label.get_height())))

test = textBox((gameScreen.get_width()/ 3, gameScreen.get_height() / 3 + 3), (200, 50), 15, "Null")
test.text = "Abcdd"
def assignMines():
    global assignedMines, amountOfMines, rows, columns
    minesLeft = amountOfMines
    while minesLeft > 0:
        if amountOfMines > (rows * columns) - 9:
            raise Exception("Too many mines! Not enough tiles!")
            break
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
            tempTile = tile((r, c), "blankTile", "blankTile", grid, gameScreen)
            tempTile.update()
            grid[tileName] = tempTile
def click(right=False, gameInfo={}):
    if loss == False and gameInitiated == True:
        if(assignedMines == False and right == False):
            assignMines()
        for i in grid:
            grid[i].click(right)
    elif gameInitiated == False:
        print(gameInfo)
        startGame(gameInfo["rows"], gameInfo["columns"], gameInfo["mines"])
def tick(): 
    topPiece = sprites["button"]
    topPiece = pygame.transform.scale(topPiece, (gameScreen.get_width(), 32))
    gameScreen.blit(topPiece, (0, 0))
    #topPieceLeft = sprites["buttonLeft"]
    #topPiece
    #topPieceLeft = pygame.transform.scale(topPieceLeft, (16, 32))
    #gameScreen.blit(topPieceLeft, (0, 0))

    for i in grid:
        

        grid[i].update()

def startGame(setRows, setColumns, mines):
    global gameScreen, amountOfMines, rows, columns, gameInitiated, gameScreen
    amountOfMines = mines
    rows = setRows
    columns = setColumns
    gameScreen = pygame.display.set_mode((((rows * sizeOfTiles)), ((columns * sizeOfTiles + (sizeOfTiles * 2)))))
    gameInitiated = True
    createGrid()


while run:
    pygame.time.Clock().tick(60)
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if gameInitiated == True:
                        click()
                    else:
                        click(False, {
                            "rows": 16,
                            "columns": 16,
                            "mines": 40
                            })
                if event.button == 3:
                    if gameInitiated == True:
                        click(True)
                    else:
                        pass
    if gameInitiated == True:    
        tick()
    elif gameInitiated == False:
        for i in range(25):
            for x in range(25):
                gameScreen.blit(sprites["blankTile"], (i * 16, x *16))
        test.draw()
    pygame.display.update() 