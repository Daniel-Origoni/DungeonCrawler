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

def moveMap(self, root):
    target0 = 350 - self.pos[0]
    target1 = 275 - self.pos[1]

    position = [0,0]

    position[0] += target0
    position[1] += target1
    move = Animation(pos = position, duration = .4)

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
        tile["position"] = [pos[0] + width / 2, pos[1] + (math.tan(1.0472) * width / 2)]
        tile["newAngle"] = 60

    if (angle == 60 and exitID == 1) or (angle == 120 and exitID == 2) or (angle == 180 and exitID == 3):
        tile["position"] = [pos[0] - width / 2, pos[1] + (math.tan(1.0472) * width / 2)]
        tile["newAngle"] = 120
        
    if (angle == 120 and exitID == 1) or (angle == 180 and exitID == 2) or (angle == 240 and exitID == 3):
        tile["position"] = [pos[0] - width, pos[1]]
        tile["newAngle"] = 180

    if (angle == 180 and exitID == 1) or (angle == 240 and exitID == 2) or (angle == 300 and exitID == 3):
        tile["position"] = [pos[0] - width / 2, pos[1] - (math.tan(1.0472) * width / 2)]
        tile["newAngle"] = 240

    if (angle == 240 and exitID == 1) or (angle == 300 and exitID == 2) or (angle == 0 and exitID == 3):
        tile["position"] = [pos[0] + width / 2, pos[1] - (math.tan(1.0472) * width / 2)]
        tile["newAngle"] = 300

    if (angle == 300 and exitID == 1) or (angle == 0 and exitID == 2) or (angle == 60 and exitID == 3):
        tile["position"] = [pos[0] + width, pos[1]]
        tile["newAngle"] = 0

    return tile

# Function to calculate if the new tile 
# would be placed on top of another
def collides(rect1, rect2):

    # Define boundries based on the passed arguments
    pointx = rect1[0][0] + (rect1[1][0] / 2)
    pointy = rect1[0][1] + (rect1[1][1] / 2)
    r2x = (rect2[0][0]) + 25
    r2y = (rect2[0][1]) + 25
    r2w = (rect2[1][0]) - 25
    r2h = (rect2[1][1]) - 25

    #Return true if the the new spot is taken
    if (pointx < r2x + r2w and pointx > r2x and pointy < r2y + r2h and pointy > r2y):
        return True
    #Return false if the new spot is available
    else:
        return False
     
def createTile(root, pos, width, height, level, angle, exitID):
        vacant = True

        tile = generateTile(angle, exitID, pos, width)

        # Use the collides() function to find vacant spot on the board.
        #If the spot is takne by any of the tiles exit the loop
        for child in root.children:
            if collides(( tile["position"], [width, height]), (child.pos, child.size)):
                vacant = False
                break
            
        # If the spot is vacant create a new tile    
        if vacant:
            root.add_widget(ImageButton(source = 'hex' + str(tile["id"]) + '.png', pos = tile["position"], level = level + 1, angle = tile["newAngle"], exitId = tile["exitId"]))

# Main class
class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Define the press() function
    def press(MyGridLayout):
        
        #Find the map layer
        child = MyGridLayout.ids.map

        #If the layer has children count how many there are
        if child.children:
            count(child)

        # If the layer has no children, create a new child
        else: 
            child.add_widget(ImageButton(pos = [child.width/2 - 50, child.height/2]))
    
    def reset(MyGridLayout):
        #Find the map layer
        MyGridLayout.ids.map.clear_widgets()
        MyGridLayout.ids.map.pos = [0,0]
        MyGridLayout.press()

# Create the ImageButton class
class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        produce = Animation(opacity = 1, duration = .75)
        produce.start(self)
    
    # Define the press() function
    def press(self):
        deactivate = Animation(opacity = 0.5, duration = .4)

        # If the tile is active
        if(self.active):

            moveMap(self, self.parent)
            
            # Create new tiles, and deactivate itself
            for digit in str(self.exitId):
                if digit == '0':
                    pass
                else:
                    createTile(self.parent, self.pos, self.width, self.height, self.level, self.angle, int(digit))

            self.active = False
            deactivate.start(self)

        # If tiles is deactivated, do nothing    
        else:
            pass
   
    
# Create the Button Class
class Button(Button):
    Button_id = ObjectProperty(None)
    pass

# Main App
class MyApp(App):
    def build(self):
        Window.clearcolor = (0,0,0,1)
        return MyGridLayout()

#Run app
if __name__ == '__main__':
    MyApp().run()

