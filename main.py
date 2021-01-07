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

'''
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
        except:
            print(Exception.__class__)

class ScrollView(GridLayout):

    def __init__(self, **kwargs):
        super(ScrollView, self).__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        try:
            with open("data_audios.json", "r") as rf:
                data = json.load(rf)
        except:
            print(Exception.__class__)
        for i in data:
            btn = Button(text=i['title'], size_hint_y=None, height=40)
            layout.add_widget(btn)
        self.add_widget(layout)
'''


class Scroll(ScrollView):
    def __init__(self, **kwargs):
        super(Scroll, self).__init__(**kwargs)
        layout = GridLayout(cols=1, size_hint_y=0.47, spacing=10)

        layout.bind(minimum_height=layout.setter('height'))  # checks when window maximized

        for i in range(1, 5):
            submit = Button(text='something', size_hint_y=None, height=40)
            layout.add_widget(submit)

        but = Button(text='Create new window!', size_hint_y=None, height=40)
        layout.add_widget(but)
        layout.add_widget(TextInput(text=''))
        self.add_widget(layout)

    def getscreen(self):
        return self.screen


class Scroll2:
    def __init__(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
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
        return


if __name__ == '__main__':
    MyApp().run()
