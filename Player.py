from kivy.uix.image import Image

class Player(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = [40,40]