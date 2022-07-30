import imp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout


class CharacterSheet(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Equipment(size_hint=(0.5, 1)))
        self.add_widget(Inventory(size_hint=(0.5, 1)))

class Slot(Label):
    pass

class Equipment(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        container = GridLayout(rows = 3, cols = 1)
        self.add_widget(container)
        bg = Image(source = "EquipmentBg.png", size_hint = (1, .8))
        container.add_widget(Label(text = "Equipment", size_hint = (1, .1), font_size = self.width/2))
        container.add_widget(bg)
        container.add_widget(Label(size_hint = (1,.1)))

class Inventory(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        container = GridLayout(rows = 3, cols = 1)
        self.add_widget(container)
        container.add_widget(Label(text = "Inventory", size_hint = (1, .1), font_size = self.width/2))

        slots = GridLayout(cols = 5, rows = 4, spacing = 10, padding = 20)
        container.add_widget(slots)
        for i in range(slots.cols * slots.rows):
            slot = RelativeLayout()
            slots.add_widget(slot)
            slot.add_widget(Image(source = "SirCulito.png"))
            slot.add_widget(Slot(text = "Slot" + str(i+1)))
        container.add_widget(Label(size_hint = (1,.1)))
            