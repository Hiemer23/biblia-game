import os

#os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.utils import platform
from kivy.core.text import LabelBase

# Importa a nossa tela recém-criada
from views.home import HomeScreen
from views.adicionar import AdicionarScreen
from views.temas import TemasScreen
from views.tema_detalhe import TemaDetalheScreen


if platform not in ('android', 'ios'):
    Window.size = (360, 640)



# Pega o diretório onde o main.py está localizado

BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, 'assets', 'fonts', 'materialdesignicons-webfont.ttf')
    
LabelBase.register(
    name='MDI', 
    fn_regular=font_path
)

# -----------------------------------------------

class MemoBibliaApp(App):
    def build(self):
        # O ScreenManager é o "gerente" que vai nos permitir trocar de telas no futuro
        gerenciador = ScreenManager()
        
        # Cadastra as duas telas no gerente
        gerenciador.add_widget(HomeScreen(name='home'))
        gerenciador.add_widget(AdicionarScreen(name='adicionar'))
        gerenciador.add_widget(TemasScreen(name='temas'))
        gerenciador.add_widget(TemaDetalheScreen(name='tema_detalhe'))
        
        gerenciador.current = 'home'
        return gerenciador

if __name__ == '__main__':
    # Dá o play no aplicativo!
    MemoBibliaApp().run()