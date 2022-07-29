
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation


class HexTile(ButtonBehavior, Image):
    def __init__(self, tiles, **kwargs):
        super().__init__(**kwargs)
        if self.pos[0] not in tiles:    
            tiles[self.pos[0]] = {}
        tiles[self.pos[0]][self.pos[1]] = self
        
    def press(self):
        deactivate = Animation(opacity = 0.3, duration = .4)
        activateAdjacent = Animation(opacity = 0.7, duration = .4)
        activateCurrent = Animation(opacity = 1, duration = .4)

        mapLayer = self.parent
        movementLayer = mapLayer.parent

        if movementLayer.isMoving:
            return

        if(self.active):
            movementLayer.moveMap(self)
            
            if not self.isParent:
                for digit in str(self.exitId):
                    if digit == '0':
                        pass
                    else: 
                        mapLayer.createTile(self, int(digit))
                        self.isParent = True

            for tile in self.adjacent:
                adjacentTile = self.parent.tiles[tile[0]][tile[1]]
                if adjacentTile.current:
                    adjacentTile.current = False
                    for origTileAdj in adjacentTile.adjacent:
                        originalTile = self.parent.tiles[origTileAdj[0]][origTileAdj[1]]
                        if originalTile != self:
                            originalTile.active = False
                            deactivate.start(originalTile)
                adjacentTile.active = True
                activateAdjacent.start(adjacentTile)
            self.current = True
            activateCurrent.start(self)
        else:
            pass
   