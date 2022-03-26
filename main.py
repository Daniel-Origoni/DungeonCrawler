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

Config.set("graphics", "width", "800")
Config.set("graphics", "height", "400")
Config.write()

# Function to count the hex Tiles
# Used for debuging
def count(target):
    print(len(target.children))


class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def __del__(self):
        Clock.unschedule(self.update)

    def press(MyGridLayout):
        produce = Animation(opacity=1, duration=1)
        child = MyGridLayout.ids.map

        if child.children:
            count(child)
        else:
            child.tiles = {child.width / 2 - 50: {}}
            child.add_widget(
                HexTile(
                    child.tiles,
                    pos=[round(child.width / 2, 2) - 50, round(child.height / 2, 2)],
                )
            )
            produce.start(child.tiles[child.width / 2 - 50][child.height / 2])

    def reset(MyGridLayout):
        MyGridLayout.ids.map.clear_widgets()
        MyGridLayout.ids.map.pos = [0, 0]
        MyGridLayout.press()

    def update(self, x):
        MapLayer.update(self.ids.map)


class Button(Button):
    Button_id = ObjectProperty(None)
    pass


class MyApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        return MyGridLayout()


if __name__ == "__main__":
    MyApp().run()
