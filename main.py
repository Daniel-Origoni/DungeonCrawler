# DungeonCrawler game
# By @Daniel-Origoni

# import dependancies
import math
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from MapLayer import HexTile
from Player import Player
from MovementLayer import MovementLayer
from CharacterSheet import CharacterSheet
from kivy.clock import Clock

Config.set('graphics', 'resizable', False)

# Function to count the hex Tiles
# Used for debuging
def count(target):
    print(len(target.children))

class MapWindow(Screen):
    pass

class InventoryWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def press(self):
        produce = Animation(opacity=1, duration=1)
        map = self.ids.map
        characters = self.ids.characters

        if len(map.children) > 1:
            count(map)
        else:
            map.tiles = {map.width / 2 - 50: {}}
            newPlayer = Player(
                pos=[
                    round(characters.width / 2, 2) - 20,
                    round(characters.height / 2, 2) + 30,
                ]
            )
            newTile = HexTile(
                map.tiles,
                pos=[round(map.width / 2, 2) - 50, round(map.height / 2, 2)],
            )
            map.add_widget(newTile)
            characters.add_widget(newPlayer)
            produce.start(
                map.tiles[round(map.width / 2, 2) - 50][round(map.height / 2, 2)]
            )

    def reset(self):
        map = self.ids.map
        charactersLayer = self.ids.characters
        player = charactersLayer.children[0]
        map.clear_widgets()
        map.pos = [0, 0]
        self.remainingTiles = {1: 0, 2: 0, 3: 0, 4: 0, 5: 2, 6: 2, 7: 2, 8: 5}
        self.remainingTiles[1] = self.remainingTiles[8] * 2 + self.remainingTiles[5] + self.remainingTiles[6] + self.remainingTiles[7] + 3
        self.remainingTiles[2] = self.remainingTiles[3] = self.remainingTiles[4] = (self.remainingTiles[1] - (self.remainingTiles[5] + self.remainingTiles[6] + self.remainingTiles[7]))
        charactersLayer.clear_widgets()
        charactersLayer.pos = [0,0]
        player.pos = [0,0]
        self.press()

    def update(self, x):
        MovementLayer.update(self.ids.base)

class Button(Button):
    Button_id = ObjectProperty(None)
    pass

kv = Builder.load_file('SirCulito.kv')

class MyApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        #Window.fullscreen = 'auto'
        return kv

if __name__ == "__main__":
    MyApp().run()
