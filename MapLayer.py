import math
from random import randint
from kivy.uix.relativelayout import RelativeLayout
from HexTile import HexTile
ROTATION_ANGLE = 60

class MapLayer(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remainingTiles = {1: 8, 2: 4, 3: 4, 4: 4, 5: 1, 6: 1, 7: 1, 8: 1}
        
    # Function to place a tile generated with generateTile() onto the board     
    def createTile(self, hexTile):

        for digit in str(hexTile.exitId):
            if digit == '0':
                pass
            else: 
                tile = generateTile(self, hexTile, int(digit))

            if tile == None:
                return
            else:    
                self.add_widget(HexTile(    self.tiles, 
                                            source = 'hex' + str(tile["id"]) + '.png', 
                                            pos = tile["position"], 
                                            angle = tile["newAngle"], 
                                            exitId = tile["exitId"], 
                                            adjacent = [hexTile.pos]
                                        ))
                hexTile.adjacent.append(tile["position"])

# Function to generate a new, random, tile.
# It calculates its new angle and position based on the previous tile. 
def generateTile(self, hexTile, exitID):
    remainingTiles = self.remainingTiles
    angle = hexTile.angle
    pos = hexTile.pos
    width = hexTile.width

    tile = {
        "id": 0,
        "exitId": 0,
        "position": [0, 0],
        "newAngle": 0,
    }
    
    #exitID can be 1, 2 or 3; by substractig 2 and multiplying it by ROTATION_ANGLE (60 degrees) we get 60, 0 or -60,
    #this number is referenced with the angle of the previous tile by adding or substracting 60, or keeping it the same.
    #To the result we add 360 and get a 360 modulo to obtain a possitive angle on the new tile.
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
    if collides(self, tile["position"], hexTile, exitID):
        return

    print("Tiles remaining: " + str(len(remainingTiles)))


    if len(remainingTiles) == 0:
        return

    #this loop adds up all remainig tiles from each kind into one total.     
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


# Function to calculate if the new tile would be placed on top of another
# and if the tiles have connecting exits 
def collides(self, position, hexTile, exitID):
    angle = hexTile.angle

    if position[0] in self.tiles:
        if position[1] in self.tiles[position[0]]:
            adjacent = False
            target = self.tiles[position[0]][position[1]]
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
                hexTile.adjacent.append(target.pos)
                target.adjacent.append(hexTile.pos)
            return True
    return False
