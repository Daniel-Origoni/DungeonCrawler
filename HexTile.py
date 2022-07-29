
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

        if(not self.disabled and not movementLayer.isMoving):
            movementLayer.moveMap(self)
            
            if not self.isParent:
                mapLayer.createTile(self)
                self.isParent = True

            for tile in self.adjacent:
                adjacentTile = self.parent.tiles[tile[0]][tile[1]]
                if adjacentTile.current:
                    adjacentTile.current = False
                    for origTileAdj in adjacentTile.adjacent:
                        originalTile = self.parent.tiles[origTileAdj[0]][origTileAdj[1]]
                        if originalTile != self:
                            originalTile.disabled = True
                            deactivate.start(originalTile)
                adjacentTile.disabled = False
                activateAdjacent.start(adjacentTile)
            self.current = True
            activateCurrent.start(self)
        else:
            pass
   