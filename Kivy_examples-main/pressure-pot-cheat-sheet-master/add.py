import os

from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.uix.scatter import Scatter
from kivy.uix.image import AsyncImage
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stencilview import StencilView

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.dropdown import DropDown

from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem, OneLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButton, \
                              MDRectangleFlatIconButton, \
                              MDFlatButton, \
                              MDRaisedButton


class CropLayout(BoxLayout, StencilView):
    path = StringProperty()

class NewFoodButton(MDFloatingActionButton):
    
    def on_release(self):
        app = MDApp.get_running_app()
        sm = app.root.ids.screen_manager
        sids = sm.screens[-1].ids
        names = ['name1', 'name2', 'cook_time', 'quick_release', 'tips', 'notes']
        
        sids.food_type.text = 'Choose ingredient type'
        sids.card.background = ''
        sids.card._no_ripple_effect = False
        sids.card_icon.icon = 'image-plus'
        sids.card_label.text = 'UPLOAD IMAGE'
        
        # Ensure no leftover crop layout
        try:
            sids.card.remove_widget(app.crop_layout)
        except:
            print('No existing crop layout')

        for name in names:
            sids[name].text = ''

        sm.transition.direction = 'left'
        sm.current = 'new_food_screen'


class FoodDropDown(DropDown):
    items = ListProperty()
    
    def create_menu_items(self):
        """Creates menu items."""

        for data in self.items:
            item = FoodListItem(
                text=data.get("text", ""),
                icon=data.get("icon", ""),
                divider='Full',
                dropdown=self,
            )
            self.add_widget(item)


class FoodListItem(OneLineIconListItem):
    icon = StringProperty()
    dropdown = ObjectProperty()

class PhotoCard(MDCard):

    img_name = StringProperty()

    def on_press(self):
        print(1)
        # Consider asking for android permissions here?

    def on_release(self):
        app = MDApp.get_running_app()
        app.file_manager_open()

        sm = app.root.ids.screen_manager
        sids = sm.screens[-1].ids
        sids.card_icon.icon = ''
        sids.card_label.text = ''

        
class DiscardButton(MDRectangleFlatIconButton):
    dialog = None
    
    def show_discard_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title='Discard New Ingredient?',
                text='Any information you entered will not be saved',
                buttons=[
                    MDFlatButton(
                        text='CANCEL', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    ),
                    MDRaisedButton(
                        text='DISCARD', 
                        md_bg_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    )
                ],
                size_hint=[.8, .5], 
                auto_dismiss=False
            )
        self.dialog.open()

    def my_callback(self, popup_widget):
        app = MDApp.get_running_app()
        sm = app.root.ids.screen_manager

        if popup_widget.text == 'DISCARD':
            self.dialog.dismiss()
            self.dialog = None
            sm.nav_dict['home_screen'].on_release(direction='right', back=True)
        else:
            self.dialog.dismiss()
            self.dialog = None
        return popup_widget.text

class AddIngredientButton(MDRectangleFlatIconButton):
    dialog = None
    screen_dict = {
        "Vegetables": "veggie_screen",
        "Meat & Eggs": "meat_screen",
        "Rice & Grains": "grain_screen",
        "Beans & Lentils": "bean_screen",
        "Seafood": "fish_screen"
    }
    
    def show_add_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title='Add New Ingredient?',
                text='Custom ingredients can be deleted at any time',
                buttons=[
                    MDFlatButton(
                        text='CANCEL', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    ),
                    MDRaisedButton(
                        text='ADD', 
                        md_bg_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    )
                ],
                size_hint=[.8, .5], 
                auto_dismiss=False
            )
        self.dialog.open()

    def show_success_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title='Success!',
                text='You successfully added a new ingredient',
                buttons=[
                    MDFlatButton(
                        text='OK', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    )
                ],
                size_hint=[.8, .5], 
                auto_dismiss=False
            )
        self.dialog.open()

    def show_error_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title='Error:',
                text='Please select ingredient type',
                buttons=[
                    MDFlatButton(
                        text='GO BACK', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    )
                ],
                size_hint=[.8, .5], 
                auto_dismiss=False
            )
        self.dialog.open()

    def my_callback(self, popup_widget):
        app = MDApp.get_running_app()
        sm = app.root.ids.screen_manager
        snames = self.screen_dict
        sids = sm.screens[-1].ids

        if popup_widget.text == 'ADD':
            try:
                picture = sids.card.img_name
                dir_path = os.path.abspath('.')
                sids.card.export_to_png(f'{dir_path}/images/{sids.card.img_name}')
                screen_name = snames[sids.food_type.text]

                self.dialog.dismiss()
                self.dialog = None
                vals = (sids.name1.text, sids.name2.text, sids.cook_time.text, sids.quick_release.text, \
                        sids.tips.text, sids.notes.text, screen_name, picture, True)

                query = '''
                    INSERT INTO ingredients (name1,name2,cook_time,quick_release,more_info,notes,screen,picture,user_added)
                    VALUES (?,?,?,?,?,?,?,?,?);
                '''
                app.cursor.execute(query, vals)
                app.conn.commit()
                sm.get_screen(screen_name).add_tile()

                self.show_success_dialog()
            except:
                # They did not choose a food type
                self.dialog.dismiss()
                self.dialog = None
                self.show_error_dialog()
        
        elif popup_widget.text == 'OK':
            # remove crop layout
            sids.card.remove_widget(app.crop_layout)

            self.dialog.dismiss()
            self.dialog = None
            sm.nav_dict['home_screen'].on_release()
        else:
            self.dialog.dismiss()
            self.dialog = None
        return popup_widget.text


class DeleteButton(MDRectangleFlatIconButton):
    dialog = None
    
    def show_delete_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title='Delete Custom Ingredient?',
                text='Custom ingredient will be deleted permenantly and cannot be recovered',
                buttons=[
                    MDFlatButton(
                        text='CANCEL', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    ),
                    MDRaisedButton(
                        text='DELETE', 
                        md_bg_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    )
                ],
                size_hint=[.8, .5], 
                auto_dismiss=False
            )
        self.dialog.open()

    def my_callback(self, popup_widget):
        app = MDApp.get_running_app()
        sm = app.root.ids.screen_manager
        detail_screen = sm.screens[-2]

        dir_path = os.path.abspath('.')
        img_path = f'{dir_path}/{detail_screen.ids.card.background}'

        if popup_widget.text == 'DELETE':
            detail_screen.ids.rl.remove_widget(app.delete_btn)
            detail_screen.ref_screen.remove_tile(detail_screen.tile)

            os.remove(img_path)
            self.dialog.dismiss()
            self.dialog = None
            sm.nav_dict['home_screen'].on_release(direction='right')
        else:
            self.dialog.dismiss()
            self.dialog = None
        return popup_widget.text