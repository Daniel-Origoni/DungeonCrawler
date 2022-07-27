# DungeonCrawler game
# By @Daniel-Origoni

# import dependancies
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from HexTile import HexTile
from MapLayer import MapLayer
from Player import Player
from kivy.clock import Clock


# Function to count the hex Tiles
# Used for debuging
def count(target):
    print(len(target.children))


class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def press(self):
        produce = Animation(opacity=1, duration=1)
        map = self.ids.map
        characters = self.ids.characters

        if len(map.children) > 1:
            count(map)
        else:
            map.tiles = {map.width / 2 - 50: {}}
            newPlayer = Player(pos=[round(characters.width / 2, 2) - 20, round(characters.height / 2, 2) + 30])
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
        map.clear_widgets()
        map.pos = [0, 0]
        map.remainingTiles = {
            1: 8,
            2: 4,
            3: 4,
            4: 4,
            5: 1,
            6: 1,
            7: 1,
            8: 1,
        }
        self.ids.characters.clear_widgets()
        self.press()

    def update(self, x):
        MapLayer.update(self.ids.map)


class Button(Button):
    Button_id = ObjectProperty(None)
    pass


class MyApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        Window.maximize()
        return MyGridLayout()


if __name__ == "__main__":
    MyApp().run()
