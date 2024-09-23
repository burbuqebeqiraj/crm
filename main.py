from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from logic.dashboard.dashboard import DashboardWindow
from logic.customer.addCustomer import AddCustomerWindow
from logic.login.login import LoginWindow
from logic.customer.viewCustomer import ViewCustomersWindow

class MyScreenManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(LoginWindow(name='login'))
        sm.add_widget(DashboardWindow(name='dashboard'))
        sm.add_widget(AddCustomerWindow(name='add_customer'))
        sm.add_widget(ViewCustomersWindow(name='view_customers'))
        return sm

if __name__ == '__main__':
    MainApp().run()
