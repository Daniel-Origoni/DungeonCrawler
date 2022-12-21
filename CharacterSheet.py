from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import ObjectProperty

M = 0.7
P = (1 - M) / 2

class CharacterSheet(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventorySlots = {1: 8, 2: 5, 3: 5, 4: 5, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}
        self.cols = 3
        self.rows = 3
        W = Window.size
        print(W)
        background = GridLayout(rows = 1, cols = 2,)

        self.add_widget(RelativeLayout(size_hint=(P, P)))
        self.add_widget(Label(size_hint=(M, P)))
        self.add_widget(Label(size_hint=(P, P)))
        self.add_widget(Label(size_hint=(P, M)))
        self.add_widget(background)
        self.add_widget(Label(size_hint=(P, M)))
        self.add_widget(Label(size_hint=(P, P)))
        self.add_widget(Label(size_hint=(M, P)))
        self.add_widget(Label(size_hint=(P, P)))

        background.add_widget(Equipment(size_hint=(0.5, 1), pos_hint={"left": 1}))
        background.add_widget(Inventory(size_hint=(0.5, 1)))


class Slot(FloatLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.txt = text

    def press(self):
        deactivate = Animation(opacity = 0, duration = .4) + Animation(opacity = 1, duration = .4)
        self.src = 'EquipmentBg.png'
        deactivate.start(self)
        pass
        

    def release(self):
        print(self.size)

class Item(ButtonBehavior, Image):
        pass

class Equipment(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        container = GridLayout(rows=3, cols=1)
        self.add_widget(container)
        equipmentTab = RelativeLayout()
        bg = Image(source="EquipmentBg.png", size_hint=(1, 0.8))

        # Title of tab "Equipment"
        container.add_widget(
            Label(text="Equipment", size_hint=(1, 0.1), font_size=self.width / 2)
        )

        # Main body of equipment tab
        container.add_widget(equipmentTab)
        equipmentTab.add_widget(bg)

        equipmentTab.add_widget(
            Slot('Potion',
                pos_hint={"left": 1, "center_y": 0.7},
                size_hint=(0.20, 0.22),
            )
        )
        equipmentTab.add_widget(
            Slot(
                text="Scroll",
                pos_hint={"right": 1, "center_y": 0.7},
                size_hint=(0.20, 0.22),
            )
        )
        equipmentTab.add_widget(
            Slot(
                text="Equip 1",
                pos_hint={"left": 1, "center_y": 0.2},
                size_hint=(0.20, 0.22),
            )
        )
        equipmentTab.add_widget(
            Slot(
                text="Equip 2",
                pos_hint={"right": 1, "center_y": 0.2},
                size_hint=(0.20, 0.22),
            )
        )

        # Foot padding for tab "Equipment"
        container.add_widget(Label(size_hint=(1, 0.1)))


class Inventory(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        container = GridLayout(rows=3, cols=1)
        self.add_widget(container)
        container.add_widget(
            Label(text="Inventory", size_hint=(1, 0.2), font_size=self.width / 2)
        )

        slots = GridLayout(cols=5, rows=4, spacing=10, padding=20)
        container.add_widget(slots)
        for i in range(slots.cols * slots.rows):
            slot = RelativeLayout()
            slots.add_widget(slot)
            slot.add_widget(Slot(text="Slot" + str(i + 1)))
        container.add_widget(Label(size_hint=(1, 0.2)))
