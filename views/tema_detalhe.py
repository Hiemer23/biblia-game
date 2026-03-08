from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle # Para desenhar o fundo dos Cards
from views.componentes import BotaoArredondado

from models.database import BancoDeDados

class TemaDetalheScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = BancoDeDados()
        self.tema_atual = ""
        
        self.layout_principal = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        self.lbl_titulo = Label(text="Tema", font_size=dp(28), size_hint=(1, 0.1), bold=True)
        self.layout_principal.add_widget(self.lbl_titulo)
        
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.grade_versiculos = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.grade_versiculos.bind(minimum_height=self.grade_versiculos.setter('height'))
        
        self.scroll.add_widget(self.grade_versiculos)
        self.layout_principal.add_widget(self.scroll)
        
        btn_voltar = BotaoArredondado(text="Voltar aos Temas", size_hint=(1, 0.1))
        btn_voltar.bind(on_release=self.voltar_temas)
        self.layout_principal.add_widget(btn_voltar)
        
        self.add_widget(self.layout_principal)

    def on_pre_enter(self, *args):
        self.lbl_titulo.text = f"Tema: {self.tema_atual}"
        self.carregar_versiculos()

    def carregar_versiculos(self):
        self.grade_versiculos.clear_widgets()
        versiculos = self.db.listar_versiculos_do_tema(self.tema_atual)
        
        if not versiculos:
            self.grade_versiculos.add_widget(Label(text="Nenhum versículo neste tema.", size_hint_y=None, height=dp(50)))
            return
            
        # O enumerate(versiculos) gera um índice (0, 1, 2...) para sabermos a cor do fundo
        for indice, v in enumerate(versiculos):
            
            # --- O CARD PRINCIPAL ---
            # Aumentamos a altura para dp(120) para caber bem o texto
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(120), padding=dp(10), spacing=dp(10))
            
            # A Mágica do Zebrado: Se for par, Cinza um pouco mais claro. Se for ímpar, Cinza escuro.
            cor_fundo = (0.22, 0.22, 0.22, 1) if indice % 2 == 0 else (0.15, 0.15, 0.15, 1)
            
            # Pinta o fundo do Card
            with card.canvas.before:
                Color(*cor_fundo)
                card.bg_rect = Rectangle(size=card.size, pos=card.pos)
            
            # Função para garantir que a cor não "descole" quando a tela rolar
            def atualizar_fundo(instancia, valor):
                instancia.bg_rect.pos = instancia.pos
                instancia.bg_rect.size = instancia.size
            card.bind(pos=atualizar_fundo, size=atualizar_fundo)
            
            # --- CAIXA DOS TEXTOS ---
            # spacing=0 deixa o título coladinho no texto debaixo
            box_textos = BoxLayout(orientation='vertical', size_hint_x=0.85, spacing=0)
            
            # 1. Referência (Livro, Cap:Vers) - Em Negrito e Maior
            lbl_ref = Label(
                text=f"[b]{v['livro']} {v['capitulo']}:{v['versiculo']}[/b]", 
                markup=True,
                font_size=dp(18),
                size_hint_y=0.35,
                halign="left",
                valign="bottom" # Empurra o texto para baixo para grudar no versículo
            )
            lbl_ref.bind(size=lbl_ref.setter('text_size'))
            
            # 2. O Texto Bíblico - Fonte Menor, Sem negrito e Cinza mais claro
            lbl_texto = Label(
                text=v['texto'],
                font_size=dp(14),
                size_hint_y=0.65,
                halign="left",
                valign="top", # Empurra o texto para cima para grudar no título
                color=(0.8, 0.8, 0.8, 1) 
            )
            lbl_texto.bind(size=lbl_texto.setter('text_size'))
            
            box_textos.add_widget(lbl_ref)
            box_textos.add_widget(lbl_texto)
            
            # --- BOTÃO EXCLUIR ---
            btn_excluir = BotaoArredondado(
                text="X", 
                cor_fundo=(0.8, 0.2, 0.2, 1),
                size_hint_x=0.15,
                font_size=dp(20),
                bold=True,
                raio=5
            )
            btn_excluir.bind(on_release=lambda btn, l=v['livro'], c=v['capitulo'], ver=v['versiculo']: self.deletar_versiculo(l, c, ver))
            
            # Junta tudo no Card
            card.add_widget(box_textos)
            card.add_widget(btn_excluir)
            
            # Adiciona o Card na lista principal
            self.grade_versiculos.add_widget(card)

    def deletar_versiculo(self, livro, capitulo, versiculo):
        sucesso, msg = self.db.remover_vinculo_tema(livro, capitulo, versiculo, self.tema_atual)
        if sucesso:
            self.carregar_versiculos()

    def voltar_temas(self, instancia):
        self.manager.transition.direction = 'right' # <-- Adicione esta linha (Voltando)
        self.manager.current = 'temas'