from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.layout import Layout
import json

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.stencilview import StencilView
from kivy.uix.textinput import TextInput


class Container(GridLayout):

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.read_songs()
        self.padding = 30
        self.spacing = 10

    def read_songs(self):
        try:
            with open("data_audios.json", "r") as rf:
                data = json.load(rf)
            length = len(data)
            if length > 10:
                length = 10
            i = 0
            for el in data:
                i += 1
                if i > length:
                    break
                lab = Button(text=el['title'])
                self.add_widget(lab)
        except Exception:
            raise


class ScrollVw(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        try:
            with open("data_audios.json", "r") as rf:
                data = json.load(rf)
        except Exception:
            raise
        for i in data:
            btn = Button(text=i['title'], size_hint_y=None, height=40)
            layout.add_widget(btn)
        self.add_widget(layout)


class ScrollT(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout()

        self.layout.cols = 1
        self.layout.size_hint_y = 0.47
        self.layout.spacing = 10

        self.layout.bind(minimum_height=self.layout.setter('height'))  # checks when window maximized

        for i in range(1, 5):
            self.submit = Button(text='something', size_hint_y=None, height=40)
            self.layout.add_widget(self.submit)

        self.add_widget(self.layout)


class Scroll2:
    def __init__(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)

        layout.bind(minimum_height=layout.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        screen = Screen(name='test')
        screen.add_widget(root)


class MyApp(App):
    def build(self):
        return ScrollT()


if __name__ == '__main__':
    MyApp().run()
