from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class Content(BoxLayout):
    pass

class InfoItem(TwoLineListItem):
    dialog = None

    def show_info_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title=self.text,
                text=self.secondary_text,
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

    def my_callback(self, popup_widget):
        self.dialog.dismiss()
        self.dialog = None
        return popup_widget.text


class NoteItem(TwoLineListItem):
    dialog = None
    food_id = NumericProperty(None)
    food_name = StringProperty(None)

    def add_note_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title=self.text,
                type='custom',
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text='CANCEL', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    ),
                    MDFlatButton(
                        text='ADD', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    )
                ],
                size_hint=[.8, 1], 
                auto_dismiss=False
            )
            self.dialog.set_normal_height()
            self.dialog.open()

    def view_note_dialog(self):
        if not self.dialog:    
            self.dialog = MDDialog(
                title=self.text,
                text=self.secondary_text,
                buttons=[
                    MDFlatButton(
                        text='CANCEL', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    ),
                    MDFlatButton(
                        text='EDIT', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    )
                ],
                size_hint=[.8, .5], 
                auto_dismiss=False
            )
        self.dialog.open()

    def edit_note_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title=self.text,
                type='custom',
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text='CANCEL', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    ),
                    MDFlatButton(
                        text='SAVE', 
                        text_color=self.theme_cls.primary_color, 
                        on_release=self.my_callback
                    )
                ],
                size_hint=[.8, 1], 
                auto_dismiss=False
            )

        self.dialog.content_cls.ids.note_text.text = self.secondary_text
        self.dialog.set_normal_height()
        self.dialog.open()

    def my_callback(self, popup_widget):
        app = MDApp.get_running_app()

        if popup_widget.text == 'EDIT':
            self.dialog.dismiss()
            self.dialog = None
            self.edit_note_dialog()
        elif popup_widget.text == 'ADD':
            query = 'UPDATE ingredients SET notes=? WHERE name1=? AND id=?;'
            vals = (self.dialog.content_cls.text, self.food_name, self.food_id)
            app.cursor.execute(query, vals)
            app.conn.commit()
            self.note_content = self.dialog.content_cls
            self.secondary_text = self.dialog.content_cls.text
            self.dialog.dismiss()
            self.dialog = None
        elif popup_widget.text == 'SAVE':
            query = 'UPDATE ingredients SET notes=? WHERE name1=? AND id=?;'
            vals = (self.dialog.content_cls.text, self.food_name, self.food_id)
            app.cursor.execute(query, vals)
            app.conn.commit()
            self.secondary_text = self.dialog.content_cls.text
            self.dialog.dismiss()
            self.dialog = None
        else:
            self.dialog.dismiss()
            self.dialog = None

        
        return popup_widget.text