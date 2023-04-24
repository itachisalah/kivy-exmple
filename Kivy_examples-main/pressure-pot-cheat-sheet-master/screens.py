import webbrowser

from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.uix.menu import MDDropdownMenu

from dialogs import InfoItem, NoteItem
from add import NewFoodButton, FoodDropDown, CropLayout


class MyScreenManager(ScreenManager):
    
    history = ['home_screen']
    nav_dict = {}

    def create_screens(self, nav_dict):
        '''
        `nav_dict` should be in this format:
        {"icon_name": ["item_text", "screen_name"], ...}
        '''
        app = MDApp.get_running_app()

        for item in nav_dict.keys():
            if nav_dict[item][1] == 'home_screen':
                self.add_widget(
                    MenuScreen(name=nav_dict[item][1],
                               title=nav_dict[item][0],
                               nav_drawer=app.root.ids.nav_drawer)
                )
            elif nav_dict[item][1] == 'credit_screen':
                self.add_widget(
                    CreditScreen(name=nav_dict[item][1],
                                 title=nav_dict[item][0],
                                 nav_drawer=app.root.ids.nav_drawer)
                )
            else:
                self.add_widget(
                StandardScreen(name=nav_dict[item][1],
                               title=nav_dict[item][0],
                               nav_drawer=app.root.ids.nav_drawer)
            )
        
        self.add_widget(IngredientScreen(nav_drawer=app.root.ids.nav_drawer))
        self.add_widget(
            NewFoodScreen(
                nav_drawer=app.root.ids.nav_drawer,
                screen_manager=self
            )
        )
    
    def go_back(self):
        prev_screen = ''
        
        self.history.pop()
        
        if self.history[-1] != 'ingredient_screen':
            prev_screen = self.history[-1]
            self.nav_dict[prev_screen].on_release(direction='right', back=True)
        else:
            self.history.pop()
            while self.history[-1] == 'ingredient_screen':
                self.history.pop()
            prev_screen = self.history[-1]
            self.nav_dict[prev_screen].on_release(direction='right', back=True)
            
        return 1
        

class IngredientScreen(MDScreen):
    nav_drawer = ObjectProperty()
    tile = ObjectProperty()
    ref_screen = ObjectProperty()


class IngredientTile(SmartTileWithLabel):
    name = StringProperty()
    detail_screen = ObjectProperty()
    id = StringProperty()

    def on_press(self):
        app = MDApp.get_running_app()
        # call db and populate ingredient screen
        query = 'SELECT * FROM ingredients WHERE name1=? AND id=?;'
        vals = (self.name, self.id)
        app.cursor.execute(query, vals)
        ingredient_info = app.cursor.fetchall()[0]
        
        details = self.detail_screen.ids
        # Set labels
        details.label1.text = ingredient_info[1]
        details.label2.text = ingredient_info[2]
        # Set image, cook time and quick release
        details.card.background = 'images/' + ingredient_info[8]
        details.cook_time.secondary_text = ingredient_info[3]
        details.quick_release.secondary_text = ingredient_info[4]
        # Send id and name to NoteItem 
        details.notes.food_id = ingredient_info[0]
        details.notes.food_name = ingredient_info[1]
        # Set tips and notes
        if ingredient_info[5] != '':
            details.tips.secondary_text = ingredient_info[5]
        else:
            details.tips.secondary_text = 'N/A'
        
        if ingredient_info[6] != '':
            details.notes.secondary_text = ingredient_info[6]
        else:
            details.notes.secondary_text = 'Add your own notes here'

        # Add delete button if custom ingredient
        if ingredient_info[12]:
            try:
                details.rl.height = app.delete_btn.height
                details.rl.add_widget(app.delete_btn)
            except:
                print(Exception)
        # Remove delete button if still exists and not custom ingredient
        else:
            try:
                details.rl.remove_widget(app.delete_btn)
                details.rl.height = 0
            except:
                print(Exception)

    def on_release(self):
        app = MDApp.get_running_app()
        sm = app.sm
        self.detail_screen.tile = self
        self.detail_screen.ref_screen = sm.current_screen
        sm.transition.direction = 'left'
        sm.current = 'ingredient_screen'
        # Add to history
        sm.history.append(sm.current)
        

class StandardScreen(MDScreen):
    name = StringProperty()
    title = StringProperty()
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    def populate_screen(self):
        app = MDApp.get_running_app()
        screen_name = self.name
        detail_screen = app.root.ids.screen_manager.screens[-2]
        query = 'SELECT * FROM ingredients WHERE screen=?;'
        vals = (screen_name,) 
        app.cursor.execute(query, vals)
        info = app.cursor.fetchall()

        for i in range(len(info)):
            self.ids.grid.add_widget(
                IngredientTile(
                    source='images/' + info[i][8],
                    text=f'[size=14sp]{info[i][1]}[/size]\n[size=10sp]{info[i][2]}[/size]',
                    name=f'{info[i][1]}',
                    id=f'{info[i][0]}',
                    detail_screen=detail_screen)
            )

    def add_tile(self):
        app = MDApp.get_running_app()
        screen_name = self.name
        query = 'SELECT * FROM ingredients WHERE screen=? ORDER BY id DESC LIMIT 1;' 
        vals = (screen_name,)
        app.cursor.execute(query, vals)
        info = app.cursor.fetchall()[0]

        self.ids.grid.add_widget(
            IngredientTile(
                source='images/' + info[8],
                text=f'[size=14sp]{info[1]}[/size]\n[size=10sp]{info[2]}[/size]',
                name=info[1],
                id=f'{info[0]}',
                detail_screen=app.root.ids.screen_manager.screens[-2])
        )

    def remove_tile(self, tile):
        app = MDApp.get_running_app()
        # Delete from database
        query = 'DELETE FROM ingredients WHERE id=?;'
        vals = (tile.id,)
        app.cursor.execute(query, vals)
        app.conn.commit()

        # delete widget from screen
        self.ids.grid.remove_widget(tile)
        #print(f'Removed tile: {tile}') 
        


class CreditScreen(MDScreen):
    name = StringProperty()
    title = StringProperty()
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    def populate_screen(self):
            screen_name = self.name

            app = MDApp.get_running_app()
            query = 'SELECT name1, credit, source, url FROM ingredients;'
            app.cursor.execute(query)
            creds = app.cursor.fetchall()

            for i in range(len(creds)):
                if creds[i][1] is not None:
                    self.ids.list.add_widget(
                        CreditListItem(
                            text=creds[i][0],
                            secondary_text=creds[i][1],
                            tertiary_text=f'on {creds[i][2]}',
                            link=creds[i][3])
                    )
                else:
                    continue


class CreditListItem(ThreeLineIconListItem):
    link = StringProperty(None)
    
    def on_release(self):
        webbrowser.open(self.link)


class NewFoodScreen(MDScreen):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = MDApp.get_running_app()
        #create dropdown menu 
        menu_items = [{'icon': key, 'text': value} for key, value in app.dial_items.items()]
        self.menu = FoodDropDown(items=menu_items)
        self.menu.create_menu_items()
        self.btn = self.ids.food_type
        self.btn.bind(on_release=self.menu.open)
        self.menu.bind(on_select=lambda instance, x: setattr(self.btn, 'text', x))
        

class MenuTile(SmartTileWithLabel):
    name = StringProperty()

    def on_release(self):
        name = self.name
        app = MDApp.get_running_app()
        sm = app.sm
        sm.nav_dict[name].on_release()


class MenuScreen(StandardScreen):
    pass

    