

from kivymd.app import MDApp
from kivymd.app import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from jsonmanager import JsonManager
from jsonmanager import SHA256


class LoginScreen(Screen):
    ...


class SignUpScreen(Screen):
    ...


class Cadastro(MDApp):
    def build(self):
        # FpsMonitoring().fps_monitor_start()
        Window.minimum_height, Window.minimum_width = 600,350
        self.screen_manager = ScreenManager()
        self.login_screen = LoginScreen(name='login')
        self.signup_screen = SignUpScreen(name='signup')
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.signup_screen)
        self.__FILE = Builder.load_file('properties.kv')
        self.__ID = self.__FILE.ids
        self.__DOMAIN: tuple = ('@gmail.com', '@outlook.com')
        return self.__FILE

    def on_start(self):
        self.theme_cls.theme_style = 'Dark'

    # metódo geral
    def change_theme(self):
        if self.theme_cls.theme_style == 'Light':
            self.theme_cls.theme_style = 'Dark'
            self.__ID.fg_pass.color = '#2096f2'
        else:
            self.theme_cls.theme_style = 'Light'
            Window.clearcolor = (234, 234, 234, 1)
            self.__ID.fg_pass.color = '#2096f2'

    # Login
    def access(self):
        __file_js: dict = JsonManager().load_file()  # mantém sempre atualizado
        if not self.__ID.gmail.error:
            if not any(domain in self.__ID.gmail.text for domain in self.__DOMAIN):
                self.__ID.gmail.error = True
                self.__ID.gmail.helper_text = 'Incorrect domain'
                self.__ID.gmail.helper_text_mode = 'on_error'
            else:
                if __file_js['email'] == SHA256(self.__ID.gmail.text):
                    self.__ID.gmail.error = False
                    self.__ID.gmail.helper_text = ''
                else:
                    self.__ID.gmail.error = self.__ID.user.error =\
                    self.__ID.pw.error = True

        if not self.__ID.user.error:
            if len(self.__ID.user.text) > 30:
                self.__ID.user.error = True
                self.__ID.user.helper_text = 'why such a big name?'
                self.__ID.user.helper_text_mode = 'on_error'
            elif len(self.__ID.user.text) == 0:
                self.__ID.user.error = True
                self.__ID.user.helper_text = 'type something'
                self.__ID.user.helper_text_mode = 'on_error'
            else:
                if __file_js['user'] == SHA256(self.__ID.user.text):
                    self.__ID.user.error = False
                    self.__ID.user.helper_text = ''
                else:
                    self.__ID.gmail.error = self.__ID.user.error =\
                    self.__ID.pw.error = True

        if not self.__ID.pw.error:
            if len(self.__ID.pw.text) < 8:
                self.__ID.pw.error = True
                self.__ID.pw.helper_text = 'your password has to be greater than or equal to 8'
                self.__ID.pw.helper_text_mode = 'on_error'
            elif __file_js['pass'] == SHA256(self.__ID.pw.text):
                self.__ID.pw.error = False
                self.__ID.pw.helper_text = ''
            else:
                self.__ID.gmail.error = self.__ID.user.error =\
                self.__ID.pw.error = True

        if not self.__ID.pw.error and not self.__ID.user.error\
           and not self.__ID.gmail.error:
            print('Logado')

    # SingUp
    def verify_sign(self):
        # Avisos
        if not self.__ID.gmail_crt.error:
            if not any(domain in self.__ID.gmail_crt.text for domain in self.__DOMAIN):
                self.__ID.gmail_crt.error = True
                self.__ID.gmail_crt.helper_text = 'Incorrect domain'
                self.__ID.gmail_crt.helper_text_mode = 'on_error'
            else:
                self.__ID.gmail_crt.error = False
                self.__ID.gmail_crt.helper_text = ''

        if not self.__ID.user_crt.error:
            if len(self.__ID.user_crt.text) > 30:
                self.__ID.user_crt.error = True
                self.__ID.user_crt.helper_text = 'why such a big name?'
                self.__ID.user_crt.helper_text_mode = 'on_error'
            elif len(self.__ID.user_crt.text) == 0:
                self.__ID.user_crt.error = True
                self.__ID.user_crt.helper_text = 'type something'
                self.__ID.user_crt.helper_text_mode = 'on_error'
            else:
                self.__ID.user_crt.error = False
                self.__ID.user_crt.helper_text = ''

        if not self.__ID.pw_crt.error and len(self.__ID.pw_crt.text) < 8:
            self.__ID.pw_crt.error = True
            self.__ID.pw_crt.helper_text = 'your password has to be greater than or equal to 8'
            self.__ID.pw_crt.helper_text_mode = 'on_error'
        else:
            self.__ID.pw_crt.error = False
            self.__ID.pw_crt.helper_text = ''

        if not self.__ID.pw_crt_vrf.error and len(self.__ID.pw_crt_vrf.text) < 8:
            self.__ID.pw_crt_vrf.error = True
            self.__ID.pw_crt_vrf.helper_text = 'your password has to be greater than or equal to 8'
            self.__ID.pw_crt_vrf.helper_text_mode = 'on_error'
        else:
            self.__ID.pw_crt_vrf.error = False
            self.__ID.pw_crt_vrf.helper_text = ''

        if not self.__ID.pw_crt_vrf.error or not self.__ID.pw_crt.error:
            if not self.__ID.pw_crt_vrf.text == self.__ID.pw_crt.text:
                self.__ID.pw_crt.error = self.__ID.pw_crt_vrf.error = True
                self.__ID.pw_crt.helper_text = self.__ID.pw_crt_vrf.helper_text = 'Passwords must be the same'
                self.__ID.pw_crt_vrf.helper_text_mode = self.__ID.pw_crt.helper_text_mode = 'on_error'
        else:
            self.__ID.pw_crt.error = self.__ID.pw_crt_vrf.error = False
            self.__ID.pw_crt.helper_text = self.__ID.pw_crt_vrf.helper_text = ''

        # Acesso
        if not self.__ID.gmail_crt.error and not self.__ID.user_crt.error and\
           not self.__ID.pw_crt.error and not self.__ID.pw_crt_vrf.error:

            # Retirando mensagem de ajuda
            self.__ID.gmail_crt.helper_text = self.__ID.user_crt.helper_text =\
                self.__ID.pw_crt.helper_text = self.__ID.pw_crt_vrf.helper_text = ''

            # Retirando o error
            self.__ID.pw_crt.error = self.__ID.pw_crt_vrf.error =\
                self.__ID.pw_crt.error = self.__ID.pw_crt_vrf.error =\
                self.__ID.user_crt.error = self.__ID.user_crt.error = False

            # Adicionando dados
            JsonManager().insert({'user': self.__ID.user_crt.text,
                                  'email': self.__ID.gmail_crt.text,
                                  'pass': self.__ID.pw_crt_vrf.text})

            print('registrado')


if __name__ == '__main__':
    Cadastro().run()
