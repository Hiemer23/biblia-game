from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from views.componentes import BotaoArredondado

COR_BOTAO_FORM = (0.3, 0.3, 0.3, 1)       # Cinza escuro
COR_BOTAO_POPUP = (0.2, 0.5, 0.8, 1)      # Azul
COR_BOTAO_SUCESSO = (0.2, 0.7, 0.3, 1)    # Verde
COR_BOTAO_VOLTAR = (0.4, 0.4, 0.4, 1)     # Cinza médio
COR_TEXTO_ERRO = (1, 0.3, 0.3, 1)         # Vermelho
COR_TEXTO_SUCESSO = (0.3, 1, 0.3, 1)      # Verde claro

ALTURA_TITULO = 0.15
ALTURA_TABELA = 0.65
ALTURA_FOOTER = 0.20

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        # O super() garante que a classe inicialize corretamente como uma Tela (Screen) do Kivy
        super().__init__(**kwargs)
        
        # Layout Principal: Uma caixa vertical que vai empilhar tudo de cima para baixo
        # padding = margem interna / spacing = espaço entre os itens
        layout_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # --- 1. CABEÇALHO ---
        lbl_titulo = Label(
            text="MemoBíblia", 
            font_size=dp(32), 
            bold=True, 
            size_hint=(1, ALTURA_TITULO)
        )
        layout_principal.add_widget(lbl_titulo)
        
        # --- 2. BLOCO DE AÇÃO (Os Jogos) ---
        box_jogos = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(1, ALTURA_TABELA))
        
        btn_palavras = BotaoArredondado(text="Palavras Ocultas", font_size=dp(20), cor_fundo=(0.3, 0.3, 0.3, 1))
        btn_referencia = BotaoArredondado(text="Onde Está Escrito?", font_size=dp(20), cor_fundo=(0.3, 0.3, 0.3, 1))
        btn_flashcards = BotaoArredondado(text="Flashcards", font_size=dp(20), cor_fundo=(0.3, 0.3, 0.3, 1))
        
        box_jogos.add_widget(btn_palavras)
        box_jogos.add_widget(btn_referencia)
        box_jogos.add_widget(btn_flashcards)
        
        layout_principal.add_widget(box_jogos)
        
        # --- 3. BLOCO DE GERENCIAMENTO (Rodapé) ---
        box_rodape = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, ALTURA_FOOTER))
        
        btn_temas = BotaoArredondado(text="Temas", font_size=dp(18), cor_fundo=(0.2, 0.5, 0.8, 1))
        btn_temas.bind(on_release=self.ir_para_temas)
        
        btn_adicionar = BotaoArredondado(text="+ Adicionar", font_size=dp(18), cor_fundo=(0.2, 0.7, 0.3, 1))
        btn_adicionar.bind(on_release=self.ir_para_adicionar)
        
        box_rodape.add_widget(btn_temas)
        box_rodape.add_widget(btn_adicionar)
        
        layout_principal.add_widget(box_rodape)
        
        # Por fim, adiciona toda essa estrutura de caixas à tela atual
        self.add_widget(layout_principal)
    
    # Adicione esta função no final da classe HomeScreen
    def ir_para_adicionar(self, instancia):
        self.manager.current = 'adicionar'
    
    def ir_para_temas(self, instancia):
        self.manager.current = 'temas'
        
    def ir_para_adicionar(self, instancia):
        self.manager.transition.direction = 'left' # <-- Adicione esta linha
        self.manager.current = 'adicionar'

    def ir_para_temas(self, instancia):
        self.manager.transition.direction = 'left' # <-- Adicione esta linha
        self.manager.current = 'temas'