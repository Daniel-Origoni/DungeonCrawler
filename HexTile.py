import math
from random import randint
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
ROTATION_ANGLE = 60

# To move the 'camera,' the entire board is shifted.
def moveMap(self, root):
    x = (root.parent.size[0]/2) - (self.size[0]/2) - self.pos[0]
    y = (root.parent.size[1]/2) - self.pos[1]
    move = Animation(pos = [x , y], duration = .4)
    move.start(root)

# Function to generate a new, random, tile.
# It calculates its new angle and position based on the previous tile.
def generateTile(exitID, self):
    remainingTiles = self.parent.remainingTiles
    angle = self.angle
    pos = self.pos
    width = self.width

    tile = {
        "id": 0,
        "exitId": 0,
        "position": [0, 0],
        "newAngle": 0,
    }
    
    angle = tile["newAngle"] = ((angle - (ROTATION_ANGLE * (exitID - 2)) + 360)%360)

    if (angle == 0):
        tile["position"] = [(pos[0] + width), (pos[1])]
    elif (angle == 60):
        tile["position"] = [(pos[0] + width / 2), (pos[1] + (math.tan(1.0472) * width / 2))]
    elif (angle == 120):
        tile["position"] = [(pos[0] - width / 2), (pos[1] + (math.tan(1.0472) * width / 2))]
    elif (angle == 180):
        tile["position"] = [(pos[0] - width), (pos[1])]
    elif (angle == 240):
        tile["position"] = [(pos[0] - width / 2), (pos[1] - (math.tan(1.0472) * width / 2))]
    else:
        tile["position"] = [(pos[0] + width / 2), (pos[1] - (math.tan(1.0472) * width / 2))]
    
    tile["position"] = [round(tile["position"][0], 2),round(tile["position"][1], 2)]

     # Use the collides() function to find vacant spot on the board.
    #If the spot is taken by any of the tiles exit the loop

    if collides(tile["position"], self, exitID):
        return

    print("Tiles remaining: " + str(len(remainingTiles)))
    if len(remainingTiles) == 0:
        return
    numberOfTiles = 0
    for typeOfTile in remainingTiles:
        numberOfTiles += (remainingTiles.get(typeOfTile))

    tileNumber = randint(1, numberOfTiles)

    print("Tile number: " + str(tileNumber))
    for typeOfTile in remainingTiles:
        if remainingTiles.get(typeOfTile) < tileNumber:
            tileNumber -= remainingTiles.get(typeOfTile)
        else:
            tile["id"] = typeOfTile
            remainingTiles[typeOfTile] -= 1
            if remainingTiles[typeOfTile] == 0:
                del remainingTiles[typeOfTile]
            break

    print("Remaining tiles: " + str(remainingTiles))

    # Establish exitId depeding on the tile selected, to be used when generating tiles based on this one.
    if tile["id"] == 4 or tile["id"] == 5 or tile["id"] == 7 or tile["id"] == 8:
        tile["exitId"] += 100
    if tile["id"] == 2 or tile["id"] == 5 or tile["id"] == 6 or tile["id"] == 8:
        tile["exitId"] += 20
    if tile["id"] == 3 or tile["id"] == 6 or tile["id"] == 7 or tile["id"] == 8:
        tile["exitId"] += 3


    return tile

# Function to calculate if the new tile 
# would be placed on top of another and
# if the tiles have matching exits 
def collides(position, self, exitID):
    angle = self.angle
    root = self.parent
    if position[0] in root.tiles:
        if position[1] in root.tiles[position[0]]:
            adjacent = False
            target = root.tiles[position[0]][position[1]]
            angle = (angle + 120 - (ROTATION_ANGLE * exitID) + 360)%360

            if target.angle == angle:
                adjacent = True
            else:
                relAng = (target.angle - angle + 360)%360
                for digit in str(target.exitId):
                    if (digit == '1' and relAng == 120) or (digit == '2' and relAng == 180) or (digit == '3' and relAng == 240):
                        adjacent = True
                        pass
            if adjacent:
                self.adjacent.append(target.pos)
                target.adjacent.append(self.pos)
            return True
    return False

# Function to place a tile generated with generateTile() onto the board     
def createTile(self, exitID):
    tile = generateTile(exitID, self)
    if tile == None:
        return
        
    self.parent.add_widget(HexTile(     self.parent.tiles, 
                                        source = 'hex' + str(tile["id"]) + '.png', 
                                        pos = tile["position"], 
                                        angle = tile["newAngle"], 
                                        exitId = tile["exitId"], 
                                        adjacent = [self.pos]
                                    ))

    self.adjacent.append(tile["position"])

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

        if(self.active):
            moveMap(self, self.parent)
            
            if not self.isParent:
                for digit in str(self.exitId):
                    if digit == '0':
                        pass
                    else: 
                        createTile(self, int(digit))
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
   