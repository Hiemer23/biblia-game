from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from views.componentes import BotaoArredondado

from models.database import BancoDeDados

class TemasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = BancoDeDados()
        
        # Layout Principal
        self.layout_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Cabeçalho
        self.layout_principal.add_widget(Label(text="Meus Temas", font_size=dp(28), size_hint=(1, 0.15), bold=True))
        
        # Área de Rolagem (ScrollView)
        self.scroll = ScrollView(size_hint=(1, 0.75))
        
        # A grade interna que vai crescer conforme o número de temas
        self.grade_temas = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.grade_temas.bind(minimum_height=self.grade_temas.setter('height'))
        
        self.scroll.add_widget(self.grade_temas)
        self.layout_principal.add_widget(self.scroll)
        
        # Botão Voltar no rodapé
        btn_voltar = BotaoArredondado(text="Voltar", size_hint=(1, 0.1))
        btn_voltar.bind(on_release=self.voltar_home)
        self.layout_principal.add_widget(btn_voltar)
        
        self.add_widget(self.layout_principal)

    def on_pre_enter(self, *args):
        """Executa toda vez que a tela está prestes a aparecer."""
        self.carregar_temas()

    def carregar_temas(self):
        # Limpa os botões antigos para não duplicar a lista ao entrar na tela novamente
        self.grade_temas.clear_widgets() 
        
        temas = self.db.listar_temas()
        
        if not temas:
            self.grade_temas.add_widget(Label(text="Nenhum tema cadastrado.", size_hint_y=None, height=dp(50)))
            return
            
        # Cria um botão para cada tema encontrado no banco
        for tema in temas:
            btn_tema = BotaoArredondado(
                text=tema['nome_tema'],
                size_hint_y=None,
                height=dp(60),
                font_size=dp(20),
                background_color=(0.2, 0.5, 0.8, 1) # Azul
            )
            
            btn_tema.bind(on_release=self.abrir_detalhes)
            self.grade_temas.add_widget(btn_tema)

    def voltar_home(self, instancia):
        self.manager.transition.direction = 'right' # <-- Adicione esta linha (Voltando)
        self.manager.current = 'home'
        
    def abrir_detalhes(self, instancia):
        # O text da instancia é o nome do botão que foi clicado (Ex: "Amor")
        nome_do_tema_clicado = instancia.text
        
        # Pega a tela de detalhes pelo Gerenciador
        tela_detalhe = self.manager.get_screen('tema_detalhe')
        
        # Injeta o nome do tema na tela de destino
        tela_detalhe.tema_atual = nome_do_tema_clicado
        
        self.manager.transition.direction = 'left' # <-- Adicione esta linha (Avançando)
        # Viaja para a tela
        self.manager.current = 'tema_detalhe'