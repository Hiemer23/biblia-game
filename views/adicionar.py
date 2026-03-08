from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from views.componentes import BotaoArredondado

from models.database import BancoDeDados

class AdicionarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = BancoDeDados()
        
        layout_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        layout_principal.add_widget(Label(text="Adicionar Versículo", font_size=dp(28), size_hint=(1, 0.15), bold=True))
        
        form_layout = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.5))
        
        # --- SPINNER: LIVRO ---
        form_layout.add_widget(Label(text="Livro:", halign="right"))
        self.spinner_livro = Spinner(
            text='Selecione o Livro',
            values=self.db.listar_livros(),
            size_hint=(1, None), height=dp(44)
        )
        self.spinner_livro.bind(text=self.ao_escolher_livro)
        form_layout.add_widget(self.spinner_livro)
        
        # --- SPINNER: CAPÍTULO ---
        form_layout.add_widget(Label(text="Capítulo:", halign="right"))
        self.spinner_capitulo = Spinner(
            text='-',
            values=[],
            size_hint=(1, None), height=dp(44),
            disabled=True # Começa bloqueado até escolher o livro
        )
        self.spinner_capitulo.bind(text=self.ao_escolher_capitulo)
        form_layout.add_widget(self.spinner_capitulo)
        
        # --- SPINNER: VERSÍCULO ---
        form_layout.add_widget(Label(text="Versículo:", halign="right"))
        self.spinner_versiculo = Spinner(
            text='-',
            values=[],
            size_hint=(1, None), height=dp(44),
            disabled=True
        )
        form_layout.add_widget(self.spinner_versiculo)
        
        # O Tema continua sendo texto livre (ou poderíamos fazer um spinner no futuro também!)
        form_layout.add_widget(Label(text="Tema:", halign="right"))
        self.input_tema = TextInput(multiline=False, size_hint=(1, None), height=dp(44))
        form_layout.add_widget(self.input_tema)
        
        layout_principal.add_widget(form_layout)
        
        self.lbl_mensagem = Label(text="", size_hint=(1, 0.1))
        layout_principal.add_widget(self.lbl_mensagem)
        
        box_botoes = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, 0.25))
        btn_voltar = BotaoArredondado(text="Voltar")
        btn_voltar.bind(on_release=self.voltar_home)
        
        btn_salvar = BotaoArredondado(text="Salvar", background_color=(0.2, 0.7, 0.3, 1))
        btn_salvar.bind(on_release=self.salvar_versiculo)
        
        box_botoes.add_widget(btn_voltar)
        box_botoes.add_widget(btn_salvar)
        
        layout_principal.add_widget(box_botoes)
        self.add_widget(layout_principal)

    # --- LÓGICA DO EFEITO DOMINÓ ---
    def ao_escolher_livro(self, spinner, livro_selecionado):
        if livro_selecionado != 'Selecione o Livro':
            # Busca os capítulos daquele livro e destrava o botão
            self.spinner_capitulo.values = self.db.listar_capitulos(livro_selecionado)
            self.spinner_capitulo.text = 'Selecione'
            self.spinner_capitulo.disabled = False
            
            # Reseta o versículo
            self.spinner_versiculo.text = '-'
            self.spinner_versiculo.values = []
            self.spinner_versiculo.disabled = True

    def ao_escolher_capitulo(self, spinner, capitulo_selecionado):
        if capitulo_selecionado not in ('-', 'Selecione'):
            livro = self.spinner_livro.text
            self.spinner_versiculo.values = self.db.listar_versiculos(livro, int(capitulo_selecionado))
            self.spinner_versiculo.text = 'Selecione'
            self.spinner_versiculo.disabled = False

    def salvar_versiculo(self, instancia):
        livro = self.spinner_livro.text
        capitulo = self.spinner_capitulo.text
        versiculo = self.spinner_versiculo.text
        tema = self.input_tema.text.strip()
        
        if livro == 'Selecione o Livro' or capitulo == 'Selecione' or versiculo == 'Selecione' or not tema:
            self.lbl_mensagem.text = "Preencha todos os campos corretamente!"
            self.lbl_mensagem.color = (1, 0.3, 0.3, 1)
            return
            
        sucesso, mensagem = self.db.vincular_versiculo_tema(livro, int(capitulo), int(versiculo), tema)
        
        self.lbl_mensagem.text = mensagem
        if sucesso:
            self.lbl_mensagem.color = (0.3, 1, 0.3, 1)
            # Reseta apenas o versículo e a mensagem para facilitar o cadastro em sequência
            self.spinner_versiculo.text = 'Selecione'
            self.input_tema.text = ""
        else:
            self.lbl_mensagem.color = (1, 0.3, 0.3, 1)


    def voltar_home(self, instancia):
        self.manager.transition.direction = 'right' # <-- Adicione esta linha
        self.manager.current = 'home'
        self.lbl_mensagem.text = ""