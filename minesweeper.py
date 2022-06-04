import pygame, sys, random
pygame.init()

sizeOfGrid = 16
lostGame = False
screenWidth, screenHeight = sizeOfGrid * 16, sizeOfGrid * 16

seed = random.randrange(1, 9994859372948, 1)
random.seed(seed)

spritesheet = pygame.image.load("spritesheet.png")
sprites = []
currentScreen = 1
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Minesweeper")
#Colors
white = (255, 255, 255)
yellow = (245, 216, 0)
black = (0, 0, 0)
darken = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
darken.fill((0, 0, 0, 0.25*255))
darken.convert_alpha()
mousePos = pygame.mouse.get_pos()
mouseX, mouseY = mousePos

def splitSprites(img, w, h, amountToSplit):
    for i in range(amountToSplit):
        returnValue = pygame.Surface((w, h)).convert_alpha()
        returnValue.blit(img, (0, 0), (w * i, 0, w, h))
        sprites.append(returnValue)
    #Shortcuts
    global blankTile
    global emptyTile
    global bombTile
    global flagTile
    global tile1
    global tile2
    global tile3
    global tile4
    global tile5
    global tile6
    global tile7
    global tile8
    global flagIndicator
    global digit1
    global digit2
    global digit3
    global digit4
    global digit5
    global digit6
    global digit7
    global digit8
    global digit9

    blankTile = 0
    flagTile = 1
    emptyTile = 2
    bombTile = 3
    tile1 = 4
    tile2 = 5
    tile3 = 6
    tile4 = 7
    tile5 = 8
    tile6 = 9
    tile7 = 10
    tile8 = 11
    flagIndicator = 12
    digit1 = 13
    digit2 = 14
    digit3 = 15
    digit4 = 16
    digit5 = 17
    digit6 = 18
    digit7 = 19
    digit8 = 20
    digit9 = 21


splitSprites(spritesheet, 16, 16, 22)

mousePos = pygame.mouse.get_pos()
run = True
#List of segments
grid = []
bombCount = 0
amountOfBombs = 40
class tile:
    def __init__(self, rect, tileValue, currentTile=blankTile,):
        self.currentTile = currentTile
        self.tileValue = tileValue
        self.rect = rect
        self.hovered = False
        self.bombsNear = 0
        self.index = 0

        self.N = 0
        self.S = 0
        self.E = 0
        self.W = 0
        self.NE = 0
        self.NW = 0
        self.SE = 0
        self.SW = 0

    def draw(self):
            window.blit(sprites[self.currentTile], (self.rect.x, self.rect.y))
            if self.hovered == True:
                window.blit(darken, (self.rect.x, self.rect.y))
    def hover(self):
        if pygame.Rect.collidepoint(self.rect, mouseX, mouseY):
            self.hovered = True
        else:
            self.hovered = False
    def countBombs(self):
        if grid[self.N].tileValue == bombTile:
            self.bombsNear += 1
        if grid[self.E].tileValue == bombTile:
            self.bombsNear += 1
        if grid[self.S].tileValue == bombTile:
            self.bombsNear += 1
        if grid[self.W].tileValue == bombTile:
            self.bombsNear += 1
        if grid[self.NE].tileValue == bombTile:
            self.bombsNear += 1
        if grid[self.SE].tileValue == bombTile:
            self.bombsNear += 1
        if grid[self.NW].tileValue == bombTile:
            self.bombsNear += 1
        if grid[self.SW].tileValue == bombTile:
            self.bombsNear += 1

    def clicked(self):
        if self.tileValue == bombTile:
            self.currentTile = self.tileValue
            loseGame(grid)
        else:
            if(self.bombsNear == 0):
                self.tileValue = emptyTile
            if(self.bombsNear == 1):
                self.tileValue = tile1
            if(self.bombsNear == 2):
                self.tileValue = tile2
            if(self.bombsNear == 3):
                self.tileValue = tile3
            if(self.bombsNear == 4):
                self.tileValue = tile4
            if(self.bombsNear == 5):
                self.tileValue = tile5
            if(self.bombsNear == 6):
                self.tileValue = tile6
            if(self.bombsNear == 7):
                self.tileValue = tile7
            if(self.bombsNear == 8):
                self.tileValue = tile8
            self.currentTile = self.tileValue
def addGrid(sizeOfSegments):
    for x in range(0, sizeOfGrid * sizeOfSegments, sizeOfSegments):
        for y in range(0, sizeOfGrid * sizeOfSegments, sizeOfSegments):
            pushSegment = tile(pygame.Rect(x,y,sizeOfSegments,sizeOfSegments), blankTile)
            pushSegment.N = pushSegment.index - 1
            pushSegment.S = pushSegment.index + 1
            pushSegment.E = pushSegment.index + sizeOfGrid
            pushSegment.W = pushSegment.index - sizeOfGrid
            pushSegment.NE = (pushSegment.index - 1) + sizeOfGrid
            pushSegment.NW = (pushSegment.index - 1) - sizeOfGrid
            pushSegment.SE = (pushSegment.index + 1) + sizeOfGrid
            pushSegment.SW = (pushSegment.index + 1) - sizeOfGrid
            pushSegment.countBombs()
            if pushSegment.N <=0:
                pushSegment.N = pushSegment.index
            if pushSegment.E <=0:
                pushSegment.E = pushSegment.index
            if pushSegment.S <=0:
                pushSegment.S = pushSegment.index
            if pushSegment.W <=0:
                pushSegment.W = pushSegment.index

            if pushSegment.N >=screenHeight:
                pushSegment.N = pushSegment.index
            if pushSegment.E >=screenWidth:
                pushSegment.E = pushSegment.index
            if pushSegment.S >=screenHeight:
                pushSegment.S = pushSegment.index
            if pushSegment.W >=screenWidth:
                pushSegment.W = pushSegment.index
            
            grid.append(pushSegment)

addGrid(16)
def addBombs(amountOfBombs):
    global bombCount
    while bombCount < amountOfBombs:
        tileOfBomb = random.randrange(0, grid.__len__())
        if grid[tileOfBomb].tileValue != bombTile:
            grid[tileOfBomb].tileValue = bombTile
            bombCount += 1
        else:
            pass
addBombs(amountOfBombs)

def drawGrid(list):
    for segment in list:
        segment.draw()
drawGrid(grid)
def mouseHover(list):
    for segment in list:
        segment.hover()
def drawMenu():
    pass
def loseGame(list):
    lostGame = True
    for segment in list:
        if segment.tileValue == bombTile:
            segment.currentTile = segment.tileValue
def mouseClicked(list):
    global mouseX, mouseY
    for segment in list:
        if pygame.Rect.collidepoint(segment.rect, mouseX, mouseY):
            segment.clicked()
while run:
    pygame.time.Clock().tick(60)
    mouseX, mouseY = mousePos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClicked(grid)
    window = pygame.display.set_mode((screenWidth, screenHeight))
    menu = pygame.display.set_mode((screenWidth, screenHeight))
    mousePos = pygame.mouse.get_pos()
    if currentScreen == 1:
        drawGrid(grid)
        mouseHover(grid)
    elif currentScreen == 2:
        window.fill(255 )
    pygame.display.update()    