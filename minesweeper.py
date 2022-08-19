from math import floor
import pygame
import os
import sys
import random
sys.setrecursionlimit(10*9)

pygame.init()

rows, columns, sizeOfTiles = 16, 16, 16
amountOfMines = 40
mineCount = 0
window = pygame.display.set_mode((rows * sizeOfTiles, columns * sizeOfTiles))
pygame.display.set_caption("Iob's PySweeper")

grid = []
spritesheet = pygame.image.load("spritesheet.png")
run = True
# Sprite Splitter


def splitSprite(sheet, x, w,  h):
    returnValue = pygame.Surface((w, h)).convert_alpha()
    returnValue.blit(sheet, (0, 0), (x, 0, w, h))
    return returnValue


# Mouse pos
mousePos = pygame.mouse.get_pos()
mouseX, mouseY = mousePos
# Mouse click types
LEFT = 1
MIDDLE = 2
RIGHT = 3


# All used sprites
blankTile = splitSprite(spritesheet, 0, sizeOfTiles, sizeOfTiles)
flagTile = splitSprite(spritesheet, 16, sizeOfTiles, sizeOfTiles)
emptyTile = splitSprite(spritesheet, 32, sizeOfTiles, sizeOfTiles)
mineTile = splitSprite(spritesheet, 48, sizeOfTiles, sizeOfTiles)
tile1 = splitSprite(spritesheet, 64, sizeOfTiles, sizeOfTiles)
tile2 = splitSprite(spritesheet, 80, sizeOfTiles, sizeOfTiles)
tile3 = splitSprite(spritesheet, 96, sizeOfTiles, sizeOfTiles)
tile4 = splitSprite(spritesheet, 112, sizeOfTiles, sizeOfTiles)
tile5 = splitSprite(spritesheet, 128, sizeOfTiles, sizeOfTiles)
tile6 = splitSprite(spritesheet, 144, sizeOfTiles, sizeOfTiles)
tile7 = splitSprite(spritesheet, 160, sizeOfTiles, sizeOfTiles)
tile8 = splitSprite(spritesheet, 176, sizeOfTiles, sizeOfTiles)
# Colors
darken = pygame.Surface((16, 16), pygame.SRCALPHA, 32)
darken.fill((0, 0, 0, 0.25*255))
darken.convert_alpha()


class tile:
    def __init__(self, rect, tileValue, tileCurrent=blankTile):
        self.rect = rect
        self.tileValue = tileValue
        self.tileCurrent = tileCurrent
        self.nearbyMines = 0
        self.rIndex = 0
        self.cIndex = 0
        self.flipped = False
        self.isEdgeTile = False
        #N = [rIndex - 1, cIndex]
        #E = [self.rIndex, cIndex + 1]
        #S = [rIndex + 1, cIndex]
        #W = [self.rIndex, cIndex - 1]
        #
        #NE = [rIndex - 1, cIndex + 1]
        #NW = [rIndex - 1, cIndex - 1]
        #SE = [rIndex + 1, cIndex + 1]
        #SW = [rIndex + 1, cIndex - 1]
        self.N = [0, 0]
        self.E = [0, 0]
        self.S = [0, 0]
        self.W = [0, 0]
        self.NE = [0, 0]
        self.NW = [0, 0]
        self.SE = [0, 0]
        self.SW = [0, 0]

    def draw(self):
        if self.flipped == True:
            self.tileCurrent = self.tileValue
        window.blit(self.tileValue, (self.rect.x, self.rect.y))
        if pygame.Rect.collidepoint(self.rect, mouseX, mouseY):
            os.system('clear')
            #print(self.rIndex, self.cIndex)
            #print((self.NW[0], self.NW[1]), ((self.N[0], self.N[1])), ((self.NE[0], self.NE[1])))
            #print((self.W[0], self.W[1]), (self.rIndex, self.cIndex), (self.E[0], self.E[1]))
            #print((self.SW[0], self.SW[1]), (self.S[0], self.S[1]), (self.SE[0], self.SE[1]))
            print(self.nearbyMines)
            window.blit(darken, (self.rect.x, self.rect.y))

    def findNeighbors(self):
        # Positions of neighbours
        # Row, Column, isCurrentTileEdge?
        self.N = [self.rIndex, self.cIndex - 1]
        self.E = [self.rIndex + 1, self.cIndex]
        self.S = [self.rIndex, self.cIndex + 1]
        self.W = [self.rIndex - 1, self.cIndex]
        #
        self.NE = [self.rIndex + 1, self.cIndex - 1]
        self.NW = [self.rIndex - 1, self.cIndex - 1]
        self.SE = [self.rIndex + 1, self.cIndex + 1]
        self.SW = [self.rIndex - 1, self.cIndex + 1]

        # if self.rIndex == 0 and self.cIndex == 0:
        #    self.NW[2] = True
        # if self.rIndex == 0 and self.cIndex == 15:
        #    self.SW[2] = True
        # if self.rIndex == 15 and self.cIndex == 0:
        #    self.NE[2] = True
        # if self.rIndex == 15 and self.cIndex == 15:
        #    self.SE[2] = True
    def stopWrapping(self):
        if self.N[0] < 0 or self.N[0] > rows - 1:
            self.N[0] = self.rIndex
            self.isEdgeTile = True
        if self.E[0] < 0 or self.E[0] > rows - 1:
            self.E[0] = self.rIndex
            self.isEdgeTile = True
        if self.S[0] < 0 or self.S[0] > rows - 1:
            self.S[0] = self.rIndex
            self.isEdgeTile = True
        if self.W[0] < 0 or self.W[0] > rows - 1:
            self.W[0] = self.rIndex
            self.isEdgeTile = True

        if self.N[1] < 0 or self.N[1] > columns - 1:
            self.N[1] = self.cIndex
            self.isEdgeTile = True
        if self.E[1] < 0 or self.E[1] > columns - 1:
            self.E[1] = self.cIndex
            self.isEdgeTile = True
        if self.S[1] < 0 or self.S[1] > columns - 1:
            self.S[1] = self.cIndex
            self.isEdgeTile = True
        if self.W[1] < 0 or self.W[1] > columns - 1:
            self.W[1] = self.cIndex
            self.isEdgeTile = True

        if self.NE[0] < 0 or self.NE[0] > rows - 1:
            self.NE[0] = self.rIndex
            self.isEdgeTile = True
        if self.SE[0] < 0 or self.SE[0] > rows - 1:
            self.SE[0] = self.rIndex
            self.isEdgeTile = True
        if self.SW[0] < 0 or self.SW[0] > rows - 1:
            self.SW[0] = self.rIndex
            self.isEdgeTile = True
        if self.NW[0] < 0 or self.NW[0] > rows - 1:
            self.NW[0] = self.rIndex
            self.isEdgeTile = True

        if self.NE[1] < 0 or self.NE[1] > columns - 1:
            self.NE[1] = self.cIndex
            self.isEdgeTile = True
        if self.SE[1] < 0 or self.SE[1] > columns - 1:
            self.SE[1] = self.cIndex
            self.isEdgeTile = True
        if self.SW[1] < 0 or self.SW[1] > columns - 1:
            self.SW[1] = self.cIndex
            self.isEdgeTile = True
        if self.NW[1] < 0 or self.NW[1] > columns - 1:
            self.NW[1] = self.cIndex
            self.isEdgeTile = True

    def searchNeighbors(self):
        self.nearbyMines = 0
        # Edge tiles count mines on the edge twice for some reason
        # Wrapping doesn't happen, they're just bad at math
        # Temporaily solved by making edge bombs give 0.5 to bomb total to edge tiles
        if grid[self.N[0]][self.N[1]].tileValue == mineTile:
            self.nearbyMines += 1
        if grid[self.E[0]][self.E[1]].tileValue == mineTile:
            self.nearbyMines += 1
        if grid[self.S[0]][self.S[1]].tileValue == mineTile:
            self.nearbyMines += 1
        if grid[self.W[0]][self.W[1]].tileValue == mineTile:
            self.nearbyMines += 1
        if grid[self.NE[0]][self.NE[1]].tileValue == mineTile:
            self.nearbyMines += 1
        if grid[self.SE[0]][self.SE[1]].tileValue == mineTile:
            self.nearbyMines += 1
        if grid[self.NW[0]][self.NW[1]].tileValue == mineTile:
            self.nearbyMines += 1
        if grid[self.SW[0]][self.SW[1]].tileValue == mineTile:
            self.nearbyMines += 1

        # if self.isEdgeTile == True:
            #self.nearbyMines = floor(self.nearbyMines)
    def changeValue(self):
        # Change tile value
        if self.tileValue != mineTile:
            if self.nearbyMines == 0:
                self.tileValue = emptyTile
            if self.nearbyMines == 1:
                self.tileValue = tile1
            if self.nearbyMines == 2:
                self.tileValue = tile2
            if self.nearbyMines == 3:
                self.tileValue = tile3
            if self.nearbyMines == 4:
                self.tileValue = tile4
            if self.nearbyMines == 5:
                self.tileValue = tile5
            if self.nearbyMines == 6:
                self.tileValue = tile6
            if self.nearbyMines == 7:
                self.tileValue = tile7
            if self.nearbyMines == 8:
                self.tileValue = tile8

    def click(self, recursion, firstClick):
        if(pygame.Rect.collidepoint(self.rect, mouseX, mouseY) or firstClick == False):
            self.tileCurrent = self.tileValue
            if self.flipped == False and self.tileCurrent != flagTile:
                self.flipped = True
                if self.tileValue == mineTile:
                    for r in range(grid.__len__()):
                        for c in range(grid[r].__len__()):
                            if grid[r][c].tileValue == mineTile:
                                grid[r][c].tileCurrent = grid[r][c].tileValue
                else:
                    if self.tileValue != emptyTile and firstClick != True:
                        recursion = False
                    elif recursion == True:
                        if grid[self.N[0]][self.N[1]].tileValue != mineTile and grid[self.N[0]][self.N[1]].tileCurrent != flagTile and grid[self.N[0]][self.N[1]].flipped == False:
                            grid[self.N[0]][self.N[1]].click(True, False)
                        if grid[self.E[0]][self.E[1]].tileValue != mineTile and grid[self.E[0]][self.E[1]].tileCurrent != flagTile and grid[self.E[0]][self.E[1]].flipped == False:
                            grid[self.E[0]][self.E[1]].click(True, False)
                        if grid[self.S[0]][self.S[1]].tileValue != mineTile and grid[self.S[0]][self.S[1]].tileCurrent != flagTile and grid[self.S[0]][self.S[1]].flipped == False:
                            grid[self.S[0]][self.S[1]].click(True, False)
                        if grid[self.W[0]][self.W[1]].tileValue != mineTile and grid[self.W[0]][self.W[1]].tileCurrent != flagTile and grid[self.W[0]][self.W[1]].flipped == False:
                            grid[self.W[0]][self.W[1]].click(True, False)
                        if grid[self.NE[0]][self.NE[1]].tileValue != mineTile and grid[self.NE[0]][self.NE[1]].tileCurrent != flagTile and grid[self.NE[0]][self.NE[1]].flipped == False:
                            grid[self.NE[0]][self.NE[1]].click(True, False)
                        if grid[self.SE[0]][self.SE[1]].tileValue != mineTile and grid[self.SE[0]][self.E[1]].tileCurrent != flagTile and grid[self.SE[0]][self.SE[1]].flipped == False:
                            grid[self.SE[0]][self.SE[1]].click(True, False)
                        if grid[self.NW[0]][self.NW[1]].tileValue != mineTile and grid[self.NW[0]][self.NW[1]].tileCurrent != flagTile and grid[self.NW[0]][self.NW[1]].flipped == False:
                            grid[self.NW[0]][self.NW[1]].click(True, False)
                        if grid[self.SW[0]][self.SW[1]].tileValue != mineTile and grid[self.SW[0]][self.SW[1]].tileCurrent != flagTile and grid[self.SW[0]][self.SW[1]].flipped == False:
                            grid[self.SW[0]][self.SW[1]].click(True, False)

    def flag(self):
        if pygame.Rect.collidepoint(self.rect, mouseX, mouseY):
            self.tileValue = mineTile
            # if self.tileCurrent == blankTile:
            #    self.tileCurrent = flagTile
            # elif self.tileCurrent == flagTile:
            #    self.tileCurrent = blankTile


def createGrid():
    global offscreenTile
    for r in range(0, rows):
        grid.append([])
        for c in range(0, columns):
            grid[r].append([])
            grid[r][c] = tile(pygame.Rect(r * sizeOfTiles, c * sizeOfTiles, sizeOfTiles, sizeOfTiles), emptyTile)
            grid[r][c].rIndex = r
            grid[r][c].cIndex = c
            grid[r][c].findNeighbors()


createGrid()


def mouseClicked(button):
    global mouseX, mouseY
    if button == LEFT:
        for r in range(rows):
            for c in range(columns):
                grid[r][c].click(True, True)
    if button == RIGHT:
        for r in range(rows):
            for c in range(columns):
                grid[r][c].flag()


def generateMines(amountOfMines):
    global mineCount
    while mineCount < amountOfMines:
        inRow = random.randrange(0, rows)
        inColumn = random.randrange(0, columns)
        if grid[inRow][inColumn].tileValue != mineTile:
            grid[inRow][inColumn].tileValue = mineTile
            mineCount += 1
            #print(mineCount, grid[inRow][inColumn].tileValue)
        else:
            pass


generateMines(amountOfMines)


def gameTick():
    for r in range(rows):
        for c in range(columns):
            grid[r][c].stopWrapping()
            grid[r][c].searchNeighbors()
            grid[r][c].changeValue()
            grid[r][c].draw()


while run:
    pygame.time.Clock().tick(60)
    mousePos = pygame.mouse.get_pos()
    mouseX, mouseY = mousePos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClicked(event.button)
    window.fill((0, 0, 0))
    gameTick()
    pygame.display.update()