import pygame 
class tile:
    def __init__(self, location: tuple, tileValue, tileSprite, gridList, surface, darkTile,tileSize=16):
        self.tileValue = tileValue
        self.tileSprite = tileSprite
        self.rect = self.tileSprite.get_rect()
        self.gridList = gridList
        self.surface = surface
        self.tileSize = tileSize
        self.darkTile = darkTile
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
    def update(self):
        if self.isShown == False:
            if self.shouldUpdate == True:
                self.surface.blit(self.tileSprite, (self.rect.x, self.rect.y))
                self.shouldUpdate = False
            if pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()):
                self.surface.blit(self.darkTile, (self.rect.x, self.rect.y))
                self.shouldUpdate = True

