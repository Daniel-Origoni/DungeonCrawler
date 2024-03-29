from kivy.animation import Animation
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
import numpy as np


class MapLayer(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(
            on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up
        )
        self.remainingTiles = {1: 4, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "d":
            self.rightPressed = True
        elif keycode[1] == "a":
            self.leftPressed = True
        elif keycode[1] == "w":
            self.upPressed = True
        elif keycode[1] == "s":
            self.downPressed = True
        else:
            return False
        return True

    def on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == "d":
            self.rightPressed = False
        elif keycode[1] == "a":
            self.leftPressed = False
        elif keycode[1] == "w":
            self.upPressed = False
        elif keycode[1] == "s":
            self.downPressed = False
        else:
            return False
        return True

    def update(self):
        if self.rightPressed:
            self.x -= 10
        if self.leftPressed:
            self.x += 10
        if self.upPressed:
            self.y -= 10
        if self.downPressed:
            self.y += 10

    # To move the 'camera,' the entire board is shifted.
    def moveMap(self, tile):
        move = Animation(
            pos=[
                ((self.size[0] / 2) - tile.pos[0] - tile.width / 2),
                ((self.size[1] / 2) - tile.pos[1] - tile.width / 4),
            ],
            duration=0.4,
        )
        move.start(self)
