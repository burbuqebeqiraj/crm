from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

# Load only the login KV file for now
Builder.load_file('view/login/login.kv')
Builder.load_file('view/dashboard/dashboard.kv')

class LoginWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.password_field
        info = self.ids.info

        uname = user.text
        passw = pwd.text

        if uname == '' or passw == '':
            info.text = '[color=#FF0000]Username and/or password required![/color]'
        else:
            if uname == 'admin' and passw == 'admin':
                #info.text = '[color=#00FF00]Logged In Successfully![/color]'
                self.manager.current = 'dashboard'
            else:
                info.text = '[color=#FF0000]Invalid username and/or password![/color]'

class MyScreenManager(ScreenManager):
    pass

class DashboardWindow(Screen):
    pass

