import math
from random import randint
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
ROTATION_ANGLE = 60

class MapLayer(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remainingTiles = {1: 0, 2: 0, 3: 0, 4: 0, 5: 2, 6: 2, 7: 2, 8: 5}
        self.remainingTiles[1] = self.remainingTiles[8] * 2 + self.remainingTiles[5] + self.remainingTiles[6] + self.remainingTiles[7] + 3
        self.remainingTiles[2] = self.remainingTiles[3] = self.remainingTiles[4] = (self.remainingTiles[1] - (self.remainingTiles[5] + self.remainingTiles[6] + self.remainingTiles[7]))

    # Function to place a tile generated with generateTile() onto the board     
    def createTile(self, hexTile):
        for digit in str(hexTile.exitId):
            tile = generateTile(self, hexTile, int(digit))
            print(tile)
            if not tile == None:
                self.add_widget(HexTile(    self.tiles, 
                                            source = 'hex' + str(tile['id']) + '.png', 
                                            pos = tile["position"],
                                            level = tile["level"], 
                                            angle = tile["newAngle"], 
                                            exitId = tile["exitId"], 
                                            adjacent = [hexTile.pos]
                                        ))
                hexTile.adjacent.append(tile["position"])

# Function to generate a new, random, tile.
# It calculates its new angle and position based on the previous tile. 
def generateTile(self, hexTile, exitID):
    if ((exitID == 0) or (len(self.remainingTiles) == 0)):
        return None

    remainingTiles = self.remainingTiles

    numberOfTiles = countTiles(remainingTiles)
    print(remainingTiles)

    tile = {}
    
    tile["newAngle"] = ((hexTile.angle - (ROTATION_ANGLE * (exitID - 2)) + 360)%360)
    setPos(tile, hexTile.width, hexTile.pos)

    # Use the collides() function to find vacant spot on the board.
    #If the spot is taken by any of the tiles exit the loop
    if collides(self, tile["position"], hexTile, exitID):
        return

    tile["level"] = hexTile.level + 1
    setId(tile, numberOfTiles, remainingTiles)
    setExitId(tile)

    return tile


# Function to calculate if the new tile would be placed on top of another
# and if the tiles have connecting exits 
def collides(self, position, hexTile, exitID):

    if (position[0] in self.tiles) and (position[1] in self.tiles[position[0]]):
        target = self.tiles[position[0]][position[1]]
        angle = (hexTile.angle + 120 - (ROTATION_ANGLE * exitID) + 360)%360
        if checkAdjacent(angle, target):
            hexTile.adjacent.append(target.pos)
            target.adjacent.append(hexTile.pos)

        return True
    else:
        return False
    
def checkAdjacent(angle, target):
    if target.angle == angle:
            return True
    else:
        relativeAng = (target.angle - angle + 360)%360
        return compareExitId(target.exitId, relativeAng)

def compareExitId(exitId, angle):
    for digit in str(exitId):
        if (digit == '1' and angle == 120) or (digit == '2' and angle == 180) or (digit == '3' and angle == 240):
            return True
    return False    
                    

#exitID can be 1, 2 or 3; by substractig 2 and multiplying it by ROTATION_ANGLE (60 degrees) we get 60, 0 or -60,
#this number is referenced with the angle of the previous tile by adding or substracting 60, or keeping it the same.
#To the result we add 360 and get a 360 modulo to obtain a possitive angle on the new tile.
def setPos(tile, width, pos):
    if (tile["newAngle"] == 0):
        tile["position"] = [(pos[0] + width), (pos[1])]
    elif (tile["newAngle"] == 60):
        tile["position"] = [(pos[0] + width / 2), (pos[1] + (math.tan(1.0472) * width / 2))]
    elif (tile["newAngle"] == 120):
        tile["position"] = [(pos[0] - width / 2), (pos[1] + (math.tan(1.0472) * width / 2))]
    elif (tile["newAngle"] == 180):
        tile["position"] = [(pos[0] - width), (pos[1])]
    elif (tile["newAngle"] == 240):
        tile["position"] = [(pos[0] - width / 2), (pos[1] - (math.tan(1.0472) * width / 2))]
    else:
        tile["position"] = [(pos[0] + width / 2), (pos[1] - (math.tan(1.0472) * width / 2))]
    
    tile["position"] = [round(tile["position"][0], 2),round(tile["position"][1], 2)]

#Count the remaning number of tiles
def countTiles(remainingTiles):
    numberOfTiles = 0
    for typeOfTile in remainingTiles:
        numberOfTiles += (remainingTiles.get(typeOfTile))
    return numberOfTiles

def setId(tile, numberOfTiles, remainingTiles):
    if tile["level"] == 10:
        tileNumber = 1
    else: 
        tileNumber = randint(remainingTiles[1] + 1, int(numberOfTiles))

    for typeOfTile in remainingTiles:
        if remainingTiles.get(typeOfTile) < tileNumber:
            tileNumber -= remainingTiles.get(typeOfTile)
        else:
            remainingTiles[typeOfTile] -= 1
            if remainingTiles[typeOfTile] == 0:
                del remainingTiles[typeOfTile]
            tile["id"] = typeOfTile
            return


# Establish exitId depeding on the tile selected, to be used when generating tiles based on this one.
def setExitId(tile):
    tile["exitId"] = 0

    if tile["id"] == 4 or tile["id"] == 5 or tile["id"] == 7 or tile["id"] == 8:
        tile["exitId"] += 100
    if tile["id"] == 2 or tile["id"] == 5 or tile["id"] == 6 or tile["id"] == 8:
        tile["exitId"] += 20
    if tile["id"] == 3 or tile["id"] == 6 or tile["id"] == 7 or tile["id"] == 8:
        tile["exitId"] += 3

class HexTile(ButtonBehavior, Image):
    def __init__(self, tiles, **kwargs):
        super().__init__(**kwargs)
        if self.pos[0] not in tiles:    
            tiles[self.pos[0]] = {}
        tiles[self.pos[0]][self.pos[1]] = self
        
    def press(self):
        mapLayer = self.parent
        movementLayer = mapLayer.parent

        if(not self.disabled and not movementLayer.isMoving):
            movementLayer.moveMap(self)
            self.pressActiveTile(mapLayer)
        else:
            pass

    def pressActiveTile(self, mapLayer):
        activateCurrent = Animation(opacity = 1, duration = .4)

        if not self.isParent:
            mapLayer.createTile(self)
            self.isParent = True

        self.setAdjacent()
        self.current = True
        activateCurrent.start(self)

    def setAdjacent(self):
        activateAdjacent = Animation(opacity = 0.7, duration = .4)
        
        for tile in self.adjacent:
            adjacentTile = self.parent.tiles[tile[0]][tile[1]]
            if adjacentTile.current:
                self.deactivateTiles(adjacentTile)
            adjacentTile.disabled = False
            activateAdjacent.start(adjacentTile)

    def deactivateTiles(self, adjacentTile):
        deactivate = Animation(opacity = 0.3, duration = .4)
        adjacentTile.current = False
        for origTileAdj in adjacentTile.adjacent:
            originalTile = self.parent.tiles[origTileAdj[0]][origTileAdj[1]]
            if originalTile != self:
                originalTile.disabled = True
                deactivate.start(originalTile)