from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.core.window import Window



class MovementLayer(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rightPressed = False
        self.leftPressed = False
        self.upPressed = False
        self.downPressed = False
        self.isMoving = False
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(
            on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up
        )
        
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
        mapLayer = self.children[1]
        charactersLayer = self.children[0]
        if self.rightPressed:
            mapLayer.x -= 5
            charactersLayer.x -= 5
        if self.leftPressed:
            mapLayer.x += 5
            charactersLayer.x += 5
        if self.upPressed:
            mapLayer.y -= 5
            charactersLayer.y -= 5
        if self.downPressed:
            mapLayer.y += 5
            charactersLayer.y += 5

    # To move the 'camera,' the entire board is shifted.
    def moveMap(self, hexTile):
        mapLayer = self.children[1]
        charactersLayer = self.children[0]
        player = charactersLayer.children[0]
        x = (self.size[0] / 2) - (hexTile.size[0] / 2) - hexTile.pos[0]
        y = (self.size[1] / 2) - hexTile.pos[1]

        move = Animation(pos=[x, y], duration=0.6)
        move.bind(on_progress = self.startedMoving)
        move.bind(on_complete = self.finishedMoving)
        move.start(mapLayer)
        move.start(charactersLayer)

        walk = Animation(
            pos=[hexTile.pos[0] + 30, hexTile.pos[1] + 30],
            duration=0.3,
        ) 
        walk.start(player)

    def startedMoving(self, *args):
        self.isMoving = True
        
    def finishedMoving(self, *args):
        self.isMoving = False