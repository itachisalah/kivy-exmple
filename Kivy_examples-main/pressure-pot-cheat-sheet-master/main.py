import sqlite3
import kivymd.utils.cropimage as crop

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast

from nav import ContentNavigationDrawer
from screens import MyScreenManager, StandardScreen, MenuScreen
from add import CropLayout, DeleteButton



class MainApp(MDApp):

    conn = None
    cursor = None

    icons_item = {
        "home": ["Home", "home_screen"],
        "corn": ["Vegetables", "veggie_screen"],
        "pig-variant": ["Meat & Eggs", "meat_screen"],
        "rice": ["Rice & Grains", "grain_screen"],
        "bowl": ["Beans & Lentils", "bean_screen"],
        "fish": ["Seafood", "fish_screen"],
        "camera": ["Credits", "credit_screen"]
    }

    dial_items = {
        "corn": "Vegetables",
        "pig-variant": "Meat & Eggs",
        "rice": "Rice & Grains",
        "bowl": "Beans & Lentils",
        "fish": "Seafood"
    }
        

    def build(self):
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.primary_hue = '800'
        self.theme_cls.accent_palette = 'Gray'
        self.theme_cls.accent_hue = '800'

        self.icon = 'logo_no_txt2.png'

        Window.softinput_mode = 'below_target'

        # create file manager for adding ingredients
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
            icon_folder='images/newfolder.png',
            icon='check'
        )

        # set file manager check button color
        fm_float_btn = self.file_manager.children[0].children[0]
        fm_float_btn.text_color=[1, 1, 1, 1]
        
        self.sm = self.root.ids.screen_manager
        
        
    def on_start(self):
        # start SQLite connection here
        self.conn = sqlite3.connect('ppcs.db')
        self.cursor = self.conn.cursor()

        icons_item = self.icons_item

        # create nav_drawer
        self.root.ids.content_drawer.create_drawer(icons_item)
        # create main and standard screens
        self.sm.create_screens(icons_item)

        # populate standard screens
        for screen in self.sm.screens[1:-2]:
            screen.populate_screen()

        # ref to photo_card on new food page
        self.photo_card = self.sm.screens[-1].ids
        self.crop_layout = CropLayout()

        self.delete_btn = DeleteButton()

    def on_stop(self):
        # close SQLite connection
        self.conn.close()

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        # retrieve image name
        if '\\' in path:
            img_name = path.split('\\')[-1]
        else:
            img_name = path.split('/')[-1]

        # add cropping layout to new food screen
        self.photo_card.card.add_widget(self.crop_layout)
        self.crop_layout.path = path
        self.photo_card.card.img_name = img_name
        self.photo_card.card._no_ripple_effect = True

        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
            elif self.sm.current == 'home_screen':
                self.stop()
            elif self.sm.current == 'new_food_screen':
                self.sm.current_screen.ids.cancel_btn.show_discard_dialog()
            else:
                self.sm.go_back()
        return True
        

if __name__ == "__main__":
    MainApp().run()