# DungeonCrawler game
# By @Daniel-Origoni

#import dependancies
import math
from random import randint
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.animation import Animation


# Function to count the hex Tiles
# Used for debuging
def count(target):
    print(len(target.children))

# To move the 'camera' the entire board is shifted.
def moveMap(self, root):
    move = Animation(pos = [(350 - self.pos[0]),(275 - self.pos[1])], duration = .4)

    move.start(root)

def generateTile(angle, exitID, pos, width):
    hex = randint(1, 8)
    tile = {
        "id": hex,
        "exitId": 0,
        "position": [0, 0],
        "newAngle": 0,
    }
        
    if hex == 4 or hex == 5 or hex == 7 or hex == 8:
        tile["exitId"] += 100
    if hex == 2 or hex == 5 or hex == 6 or hex == 8:
        tile["exitId"] += 20
    if hex == 3 or hex == 6 or hex == 7 or hex == 8:
        tile["exitId"] += 3
    if (angle == 0 and exitID == 1) or (angle == 60 and exitID == 2) or (angle == 120 and exitID == 3):
        tile["position"] = [(pos[0] + width / 2), (pos[1] + (math.tan(1.0472) * width / 2))]
        tile["newAngle"] = 60
    if (angle == 60 and exitID == 1) or (angle == 120 and exitID == 2) or (angle == 180 and exitID == 3):
        tile["position"] = [(pos[0] - width / 2), (pos[1] + (math.tan(1.0472) * width / 2))]
        tile["newAngle"] = 120
    if (angle == 120 and exitID == 1) or (angle == 180 and exitID == 2) or (angle == 240 and exitID == 3):
        tile["position"] = [(pos[0] - width), (pos[1])]
        tile["newAngle"] = 180
    if (angle == 180 and exitID == 1) or (angle == 240 and exitID == 2) or (angle == 300 and exitID == 3):
        tile["position"] = [(pos[0] - width / 2), (pos[1] - (math.tan(1.0472) * width / 2))]
        tile["newAngle"] = 240
    if (angle == 240 and exitID == 1) or (angle == 300 and exitID == 2) or (angle == 0 and exitID == 3):
        tile["position"] = [(pos[0] + width / 2), (pos[1] - (math.tan(1.0472) * width / 2))]
        tile["newAngle"] = 300
    if (angle == 300 and exitID == 1) or (angle == 0 and exitID == 2) or (angle == 60 and exitID == 3):
        tile["position"] = [(pos[0] + width), (pos[1])]
        tile["newAngle"] = 0
    tile["position"][0] = round(tile["position"][0], 2)
    tile["position"][1] = round(tile["position"][1], 2)

    return tile

# Function to calculate if the new tile 
# would be placed on top of another
def collides(position, root):
    if position[0] in root.tiles:
        if position[1] in root.tiles[position[0]]:
            return True
    return False

# Function to place a tile generated with generateTile() onto the board     
def createTile(self, exitID):
    vacant = True
    tile = generateTile(self.angle, exitID, self.pos, self.width)

    # Use the collides() function to find vacant spot on the board.
    #If the spot is taken by any of the tiles exit the loop
    
    if collides(tile["position"], self.parent):
        vacant = False
        
    # If the spot is vacant create a new tile    
    if vacant:
        self.parent.add_widget(ImageButton(self.parent.tiles, source = 'hex' + str(tile["id"]) + '.png', pos = tile["position"], angle = tile["newAngle"], exitId = tile["exitId"], adjacent = [self.pos]))
        self.adjacent.append(tile["position"])
    

class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def press(MyGridLayout):
        produce = Animation(opacity = 1, duration = .75)
        child = MyGridLayout.ids.map

        if child.children:
            count(child)
            print(child.tiles)
        else: 
            child.tiles = {child.width/2-50: {}}
            child.add_widget(ImageButton(child.tiles, pos = [round(child.width/2, 2) - 50, round(child.height/2, 2)]))
            produce.start(child.tiles[child.width/2 - 50][child.height/2])
            
            
    def reset(MyGridLayout):
        MyGridLayout.ids.map.clear_widgets()
        MyGridLayout.ids.map.pos = [0,0]
        MyGridLayout.press()

class ImageButton(ButtonBehavior, Image):
    def __init__(self, tilesList, **kwargs):
        super().__init__(**kwargs)
        
        
        if self.pos[0] not in tilesList:    
            tilesList[self.pos[0]] = {}
        tilesList[self.pos[0]][self.pos[1]] = self
        
    def press(self):
        deactivate = Animation(opacity = 0.5, duration = .4)
        activate = Animation (opacity = 1, duration = .4 )

        if(self.active):
            moveMap(self, self.parent)
            
            for digit in str(self.exitId):
                if digit == '0':
                    pass
                else: 
                    createTile(self, int(digit))

            for tile in self.adjacent:
                if self.parent.tiles[tile[0]][tile[1]].current:
                    self.parent.tiles[tile[0]][tile[1]].current = False
                    
                    for origTileAdj in self.parent.tiles[tile[0]][tile[1]].adjacent:
                        if self.parent.tiles[origTileAdj[0]][origTileAdj[1]] != self:
                            self.parent.tiles[origTileAdj[0]][origTileAdj[1]].active = False
                            deactivate.start(self.parent.tiles[origTileAdj[0]][origTileAdj[1]])
                self.parent.tiles[tile[0]][tile[1]].active = True
                activate.start(self.parent.tiles[tile[0]][tile[1]])
            self.current = True
        else:
            pass
   
class Button(Button):
    Button_id = ObjectProperty(None)
    pass

class MyApp(App):
    def build(self):
        Window.clearcolor = (0,0,0,1)
        return MyGridLayout()

if __name__ == '__main__':
    MyApp().run()
