from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation


class MovementLayer(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isMoving = False

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
            pos=[player.x - (x - mapLayer.x), player.y - (y - mapLayer.y)],
            duration=0.3,
        ) 
        walk.start(player)

    def startedMoving(self, *args):
        self.isMoving = True
        
    def finishedMoving(self, *args):
        self.isMoving = False