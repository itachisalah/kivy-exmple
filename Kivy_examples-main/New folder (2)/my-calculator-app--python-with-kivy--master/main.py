from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_file("design.kv")

class SpecialFunctions:
    def truncate_long_number(answer, max_char = 10):
        """ Takes in a numeric value or string representation of a numeric value
        and produces a string with scientific notation.
        Second parameter is max_char default is 10. This limits the output number 
        to a max 10 characters. The output can be easily converted back to numeric. """
        chars_in_answer = len(str(answer))
        chars_in_lhs = len(str(int(float(answer))))
        chars_in_rhs = chars_in_answer - chars_in_lhs
        
        if chars_in_answer >= 10:
            if chars_in_lhs > chars_in_rhs:
                trunc_answer = str(float(answer) / (10**(chars_in_lhs - (max_char - 3))))
                trunc_answer = trunc_answer[0:7]
                trunc_answer = trunc_answer + "e+" + str(chars_in_lhs - 7)
            else:
                trunc_answer = str(round(answer,(max_char - chars_in_lhs)))
        else:
            trunc_answer = answer
        return trunc_answer


class MainScreen(Screen):
    numstring = ""
    active_operator = ""
    firstnumber = ""
    secondnumber = ""
    answer = 0
    has_equals_clicked = False

    def add_to_numstring(self, new):
        if MainScreen.has_equals_clicked:
            self.clear_all()

        if new == "." and "." in MainScreen.numstring:
            return
        elif len(MainScreen.numstring) >= 10:
            return
        else:
            MainScreen.numstring = MainScreen.numstring + new
            self.ids.display.text = MainScreen.numstring

    def backspace(self):
        if len(MainScreen.numstring) <= 1:
            MainScreen.numstring = ""
            self.ids.display.text = "0"
        else:
            MainScreen.numstring = MainScreen.numstring[:-1]
            self.ids.display.text = MainScreen.numstring

    def clear_all(self):
        self.ids.display.text = "0"
        self.ids.display_top.text = ""
        MainScreen.numstring = ""
        MainScreen.firstnumber = ""
        MainScreen.secondnumber = ""
        MainScreen.answer = 0
        MainScreen.active_operator = ""
        MainScreen.has_equals_clicked = False
    
    def operator_clicked(self,operator):
        MainScreen.active_operator = operator
        if MainScreen.has_equals_clicked:
            MainScreen.firstnumber = str(MainScreen.answer)
            MainScreen.has_equals_clicked = False
        elif MainScreen.numstring == "":
            MainScreen.numstring = "0"
        else:
            MainScreen.firstnumber = MainScreen.numstring.lstrip('0')
        self.ids.display_top.text = MainScreen.firstnumber + " " + MainScreen.active_operator
        MainScreen.numstring = ""
        self.ids.display.text = "0"
        
    def equals_clicked(self):
        if MainScreen.has_equals_clicked:
            return
        else:
            MainScreen.has_equals_clicked = True
            if MainScreen.numstring == "":
                MainScreen.numstring = "0"
            elif MainScreen.firstnumber == "":
                MainScreen.answer = float(MainScreen.numstring)
            else:
                try:
                    MainScreen.secondnumber = MainScreen.numstring.lstrip('0')
                    MainScreen.answer = eval(MainScreen.firstnumber + MainScreen.active_operator + MainScreen.secondnumber)
                except SyntaxError:
                    return

            # making sure the number fits on the display
            MainScreen.answer = SpecialFunctions.truncate_long_number(MainScreen.answer)

            self.ids.display_top.text = self.ids.display_top.text + " " + MainScreen.secondnumber
            self.ids.display.text =  str(MainScreen.answer)
            MainScreen.numstring = ""

    
class RootWidget(ScreenManager):
    pass


class WeeCalculator(App):
    def build(self):
        self.icon = r'icon2.png'    # change this to the actual icon
        return RootWidget()
    

if __name__ == "__main__":
    # Window.size = ((720*0.5), (1280*0.5)) # used for on PC
    Window.fullscreen = True # used for on mobile
    WeeCalculator().run()
# End