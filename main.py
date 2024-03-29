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
from kivy.config import Config
from kivy.clock import Clock


# Function to count the hex Tiles
# Used for debuging
def count(target):
    print(len(target.children))


class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def press(MyGridLayout):
        produce = Animation(opacity=1, duration=1)
        child = MyGridLayout.ids.map

        if child.children:
            count(child)
        else:
            child.tiles = {child.width / 2 - 50: {}}
            newTile = HexTile(
                child.tiles,
                pos=[round(child.width / 2, 2) - 50, round(child.height / 2, 2)],
            )
            child.add_widget(newTile)
            produce.start(
                child.tiles[round(child.width / 2, 2) - 50][round(child.height / 2, 2)]
            )

    def reset(MyGridLayout):
        MyGridLayout.ids.map.clear_widgets()
        MyGridLayout.ids.map.pos = [0, 0]
        MyGridLayout.ids.map.remainingTiles = {
            1: 4,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
            8: 1,
        }
        MyGridLayout.press()

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
