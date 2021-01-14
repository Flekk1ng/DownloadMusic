import json
import os
import threading
import audios_main

from kivy import Config
from kivy.clock import Clock
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
from kivymd.uix.list import MDList, ImageLeftWidget, OneLineRightIconListItem, ThreeLineAvatarListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.toolbar import MDToolbar


Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '760')
Config.write()
Window.size = (360, 760)


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
    orientation: "vertical"
    
    Widget:
    
    MDSpinner:
        size_hint: None, None
        size: dp(45), dp(45)
        pos_hint: {'center_x': .5, 'center_y': 1}
        active: True
    
    Widget:

           
"""


class MyApp(MDApp):
    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)

    def build(self):
        screen = Builder.load_string(kv)
        return screen

    def open_nav_drawer(self):
        self.root.ids.mscr.ids.nav_drawer.set_state('open')

    def on_stop(self):
        delete_photos()

    def on_resume(self):
        delete_photos()

    def on_pause(self):
        delete_photos()


flag = None


def sync(*args):
    global flag
    vk_session = audios_main.get_session()
    if vk_session is None:
        print('Session is None!')
        audios_main.main()
        audios_main.auth_vk()
        vk_session = audios_main.get_session()
    audios_main.update_audios(vk_session=vk_session)
    flag = True


class MainScreenLayout(BoxLayout):
    dialog = None
    dialog_spin = None
    global flag, my

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.toolbar = MDToolbar(title='My music')
        self.toolbar.elevation = 10
        self.toolbar.type = 'top'
        self.toolbar.left_action_items = [['menu', lambda x: my.root.ids.mscr.ids.nav_drawer.set_state('open')]]

        self.add_widget(self.toolbar)
        self.add_scroll_widget()

    def add_scroll_widget(self):
        sc = ScrollOne()
        self.scroll_self = sc.get_self()
        self.add_widget(self.scroll_self)

    def reload_scroll(self):
        try:
            self.remove_widget(self.scroll_self)
            self.add_scroll_widget()

        except Exception as ex:
            print(ex)

    def dialog_close(self, instance):
        self.dialog.dismiss()

    def dialog_spin_func(self):
        self.dialog_spin = MDDialog(title='Loading...',
                                    size_hint=(.7, None),
                                    auto_dismiss=False,
                                    type="custom",
                                    content_cls=Content())
        self.dialog_spin.open()

    def check_flag(self, *args):
        if flag:
            self.dialog_spin.dismiss()
            self.reload_scroll()
            self.schedule.cancel()

    def sync_music(self, instance):
        self.dialog.dismiss()
        self.dialog_spin_func()
        threading.Thread(target=sync, daemon=True).start()
        self.schedule = Clock.schedule_interval(self.check_flag, 1)
        self.schedule()

    def show_dialog_login(self):
        self.dialog = MDDialog(type="custom",
                               size_hint=(.7, None),
                               auto_dismiss=False,
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
    pass


class NavDrawer(MDNavigationDrawer):
    pass


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

    def get_self(self):
        return self


if __name__ == '__main__':
    my = MyApp()
    my.run()
