import math
from random import randint
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
ROTATION_ANGLE = 60

# To move the 'camera,' the entire board is shifted.
def moveMap(self, root):
    move = Animation(pos = [(350 - self.pos[0]),(275 - self.pos[1])], duration = .4)
    move.start(root)

# Function to generate a new, random, tile.
# It calculates its new angle and position based on the previous tile.
def generateTile(angle, exitID, pos, width):
    hex = randint(1, 8)
    tile = {
        "id": hex,
        "exitId": 0,
        "position": [0, 0],
        "newAngle": 0,
    }

    angle = tile["newAngle"] = ((angle - (ROTATION_ANGLE * (exitID - 2)) + 360)%360)

    # Establish exitId depeding on the tile selected, to be used when generating tiles based on this one.
    if hex == 4 or hex == 5 or hex == 7 or hex == 8:
        tile["exitId"] += 100
    if hex == 2 or hex == 5 or hex == 6 or hex == 8:
        tile["exitId"] += 20
    if hex == 3 or hex == 6 or hex == 7 or hex == 8:
        tile["exitId"] += 3

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
    
    tile["position"][0] = round(tile["position"][0], 2)
    tile["position"][1] = round(tile["position"][1], 2)

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
    vacant = True
    tile = generateTile(self.angle, exitID, self.pos, self.width)

    # Use the collides() function to find vacant spot on the board.
    #If the spot is taken by any of the tiles exit the loop
    if collides(tile["position"], self, exitID):
        vacant = False

    # If the spot is vacant create a new tile    
    if vacant:
        self.parent.add_widget(ImageButton(self.parent.tiles, source = 'hex' + str(tile["id"]) + '.png', pos = tile["position"], angle = tile["newAngle"], exitId = tile["exitId"], adjacent = [self.pos]))
        self.adjacent.append(tile["position"])

class ImageButton(ButtonBehavior, Image):
    def __init__(self, tilesList, **kwargs):
        super().__init__(**kwargs)
    
        if self.pos[0] not in tilesList:    
            tilesList[self.pos[0]] = {}
        tilesList[self.pos[0]][self.pos[1]] = self
        
    def press(self):
        deactivate = Animation(opacity = 0.1, duration = .4)
        activateAdjacent = Animation(opacity = 0.5, duration = .4)
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
   