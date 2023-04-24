from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp

from kivymd.uix.textfield import MDTextField
# Define screens
class HomeScreen(Screen):
    def log(self):
        username = self.ids.user.text
        password= self.ids.passw.text
        if username == 'a' and password=='1':
            app = MDApp.get_running_app()
            app.root.current = 'about_screen' 
            self.manager.transition.direction='left'


class AboutScreen(Screen):
    pass


# Define screen manager
class MyScreenManager(ScreenManager):
    pass


# Create app
class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette='Blue'
        self.theme_cls.primary_hue='300'
        self.theme_cls.theme_style="Light"
        Builder.load_file('main.kv')

        # Create screen manager and add screens
        sm = MyScreenManager()
        sm.add_widget(HomeScreen(name='home_screen'))
        sm.add_widget(AboutScreen(name='about_screen'))

        return sm
    

if __name__ == '__main__':
    MainApp().run()
