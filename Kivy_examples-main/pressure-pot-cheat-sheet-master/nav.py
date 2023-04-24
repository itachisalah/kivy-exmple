from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.list import MDList, OneLineIconListItem


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    screen_name = StringProperty()

    def on_release(self, direction='left', back=False):
        app = MDApp.get_running_app() 
        self.parent.set_color_item(self)
        app.root.ids.nav_drawer.set_state("close")
        app.sm.transition.direction = direction
        app.sm.current = self.screen_name
        # Add to History
        if not back:
            app.sm.history.append(app.sm.current)


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    # create_drawer function?
    def create_drawer(self, nav_dict):
        '''
        `nav_dict` should be in this format:
        {"icon_name": ["item_text", "screen_name"], ...}
        '''
        for item in nav_dict.keys():
            self.ids.md_list.add_widget(
                ItemDrawer(icon=item, 
                           text=nav_dict[item][0],
                           screen_name=nav_dict[item][1]
                           )
            )
            
        for item in self.ids.md_list.children:
            self.screen_manager.nav_dict.update({item.screen_name: item})


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when you tap on a menu item.'''

        #Set the color of the icon and text for the menu item
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color