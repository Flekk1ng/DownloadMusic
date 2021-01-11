import json
import os
import time

from kivy import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarListItem, ImageLeftWidget, OneLineRightIconListItem, \
    ThreeLineAvatarListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.toolbar import MDToolbar

import audios_main

"""Config.set('resizable', 'width', '0')
Config.set('resizable', 'height', '0')"""
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '760')
Config.write()

Window.size = (360, 760)


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


def delete_photos():
    try:
        with open("filenames.json", "r") as read_file:
            filenames = json.load(read_file)

        for filename in filenames:
            os.remove(filename)
    except Exception:
        raise


kv = """
MainScreenManager:
    
    MainScreen:
        id: mscr
    LoginScreen:

<MainScreen>:
    id: mscr
    name: 'main'
    NavigationLayout:
        id: navlay
        ScreenManager:
            id: scrman
            Screen:
                id: scr
                name: 'nav_screen'
                MainScreenLayout:
                    id: mainscrlayout
                    orientation: 'vertical'
                    MDToolbar:
                        type: 'top'
                        title: 'My music'
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('open')]]
                        
        NavDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: 'vertical'
                padding: "8dp"
                spacing: "8dp"
                    
                NavList:
                    id: nav_list
                        
                    OneLineIconListItem:
                        text: "Login vk"
                            
                        on_release: root.manager.current = 'login_screen'
                                                
                        IconLeftWidget:
                            icon: "login"
                                                
                    OneLineIconListItem:
                        text: 'Sync music'
                                            
                        on_release: mainscrlayout.show_dialog_login()
                                            
                        IconLeftWidget:
                            icon: 'sync'
                       
                MDFillRoundFlatButton:
                    text: "Login VK"
                    font_size: "25sp"
                    custom_color: 0, 1, 0, 1
                    pos_hint: {'center_x': 0.33, 'center_y': 0.5}
                Widget:
                    
<LoginScreen>:
    name: 'login_screen'
    AnchorLayout:
        BoxLayout:
            orientation: 'vertical'
            size_hint: 0.5, 0.5  
            spacing: 10
            Image:
                source: 'spr/music_logov2.png'
                size: self.texture_size
            MDTextField:
                hint_text: "Login"
                mode: "rectangle"
            MDTextField:
                hint_text: "Password"
                icon_right: "eye"
                password: True
                mode: "rectangle"
            MDFillRoundFlatButton
                icon: "android"
                text: 'Log in'
                pos_hint: {"center_x": .5, "center_y": .5}
                font_size: '20sp'
                
<Content>
    orientation: "horizontal"
    spacing: 13
    padding: 0
    
    MDSpinner:
        size_hint: None, None
        size: dp(35), dp(35)
        pos_hint: {'center_x': .2, 'center_y': .5}
        active: True
    MDLabel:
        text: "Loadind..."
        pos_hint: {'center_x': .8, 'center_y': .5}

                
"""


class MyApp(MDApp):

    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)

    def build(self):
        screen = Builder.load_string(kv)
        return screen

    def show_dialog_login(self):
        self.dialog = MDDialog(type="custom",
                               size_hint=(.7, .6),
                               text="Do you want to sync your music?",
                               buttons=[MDFlatButton(text="CANCEL",
                                                     text_color=self.theme_cls.primary_color,
                                                     on_press=self.dialog_close),
                                        MDFlatButton(text="SYNC",
                                                     text_color=self.theme_cls.primary_color,
                                                     on_press=self.sync_music)], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)

    def sync_music(self, instance):
        self.root.ids.mscr.ids.but.text = 'YESSSSSSSSSS'

    def open_nav_drawer(self):
        self.root.ids.mscr.ids.nav_drawer.set_state('open')


    def on_stop(self):
        delete_photos()

    def on_resume(self):
        delete_photos()

    def on_pause(self):
        delete_photos()


class MainScreenLayout(BoxLayout):

    dialog = None
    dialog_spin = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_scroll_widget()
        """self.ToolBarOne = MDToolbar(title='My music',
                                    elevation=10,
                                    left_action_items=[['menu'],
                                                       lambda x: MDApp.root.ids.mscr.ids.nav_drawer.set_state('open')])"""
        """title: 'My music'
        elevation: 10
        left_action_items: [['menu', lambda x: nav_drawer.set_state('open')]]"""

    def add_scroll_widget(self):
        sc = ScrollOne()
        self.sx = sc.getself()
        self.add_widget(self.sx)

    def reload_scroll(self):
        try:
            self.remove_widget(self.sx)
            self.add_scroll_widget()

        except Exception as ex:
            print(ex)

    def dialog_close(self, instance):
        self.dialog.dismiss()

    def dialog_spin_(self):
        self.dialog_spin = MDDialog(size_hint=(.45, None),
                                    auto_dismiss=True,
                                    type="custom",
                                    content_cls=Content())
        self.dialog_spin.open()

    def sync_music(self, instance):
        self.dialog.dismiss()
        self.dialog_spin_()
        vk_session = audios_main.get_session()
        if vk_session is None:
            print('Session is None')
            audios_main.main()
            audios_main.auth_vk()
            vk_session = audios_main.get_session()
        audios_main.update_audios(vk_session=vk_session)
        self.reload_scroll()
        self.dialog_spin.dismiss()


    def show_dialog_login(self):
        self.dialog = MDDialog(type="custom",
                               size_hint=(.7, .6),
                               text="Do you want to sync your music?",
                               buttons=[MDFlatButton(text="CANCEL",
                                                     on_press=self.dialog_close),
                                        MDFlatButton(text="SYNC",
                                                     on_press=self.sync_music)])
        self.dialog.open()


class Content(BoxLayout):
    pass


class MainScreenManager(ScreenManager):
    pass


class MainScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class NavList(MDList):

    def login(self):
        import audios_main
        pass

    def test(self):
        pass


class NavDrawer(MDNavigationDrawer):

    def test(self):
        print(1)


class ScrollOne(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import wget

        self.layout = MDList()
        self.layout.spacing = 10

        filenames = []

        try:
            with open("data_audios.json", "r") as rf:
                data = json.load(rf)
            if len(data) == 0:
                sync_but = MDFillRoundFlatIconButton(text='Sync music', icon='sync', on_press=audios_main.main())
                self.add_widget(sync_but)
            else:
                for i in data[:10]:
                    try:
                        filename = wget.download(i['track_covers'][0])
                        filenames.append(filename)
                        image = ImageLeftWidget(source=filename)
                    except Exception as ex:
                        image = ImageLeftWidget(source='spr/music_logo.png')
                        print(ex)
                    self.test = OneLineRightIconListItem
                    self.item = ThreeLineAvatarListItem(text=i['title'],
                                                        secondary_text=i['artist'],
                                                        tertiary_text=str(i['duration'][0]) + ':' + str(
                                                            i['duration'][1]))
                    self.item.add_widget(image)
                    self.layout.add_widget(self.item)

                try:
                    with open('filenames.json', 'w') as write_file:
                        json.dump(filenames, write_file, sort_keys=True, indent=4)
                except Exception as ex:
                    print(ex)

                self.add_widget(self.layout)

        except Exception as ex:
            print(ex)

    def getself(self):
        return self


if __name__ == '__main__':
    MyApp().run()
