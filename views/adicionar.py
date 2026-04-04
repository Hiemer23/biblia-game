from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.uix.textinput import TextInput

from models.database import BancoDeDados
from views.componentes import BotaoArredondado

# ==========================================
# CONFIGURAÇÕES DE DESIGN (TEMA DA TELA)
# ==========================================
ALTURA_BOTAO_FORM = dp(60) # Aumentamos de 44 para 60!
ALTURA_BOTAO_POPUP = dp(60)
ESPACO_PADRAO = dp(10)

COR_BOTAO_FORM = (0.3, 0.3, 0.3, 1)       # Cinza escuro
COR_BOTAO_POPUP = (0.2, 0.5, 0.8, 1)      # Azul
COR_BOTAO_SUCESSO = (0.2, 0.7, 0.3, 1)    # Verde
COR_BOTAO_VOLTAR = (0.4, 0.4, 0.4, 1)     # Cinza médio
COR_TEXTO_ERRO = (1, 0.3, 0.3, 1)         # Vermelho
COR_TEXTO_SUCESSO = (0.3, 1, 0.3, 1)      # Verde claro

ALTURA_TITULO = 0.15
ALTURA_TABELA = 0.65
ALTURA_FOOTER = 0.20

class AdicionarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = BancoDeDados()
        
        layout_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        layout_principal.add_widget(Label(text="Adicionar Versículo", font_size=dp(28), size_hint=(1, ALTURA_TITULO), bold=True))
        
        # Usando a variável de espaçamento
        form_layout = GridLayout(cols=2, spacing=ESPACO_PADRAO, size_hint=(1, ALTURA_TABELA))
        
        # --- BOTÃO: LIVRO ---
        form_layout.add_widget(self.criar_label_alinhado("Livro:"))
        self.btn_livro = BotaoArredondado(text='Selecione o Livro', size_hint=(1, 1), height=ALTURA_BOTAO_FORM, cor_fundo=COR_BOTAO_FORM)
        self.btn_livro.bind(on_release=self.abrir_seletor_livros)
        form_layout.add_widget(self.btn_livro)
        
        # --- BOTÃO: CAPÍTULO ---
        form_layout.add_widget(self.criar_label_alinhado("Capítulo:"))
        self.btn_capitulo = BotaoArredondado(text='-', size_hint=(1, 1), height=ALTURA_BOTAO_FORM, disabled=True, cor_fundo=COR_BOTAO_FORM)
        self.btn_capitulo.bind(on_release=self.abrir_seletor_capitulos)
        form_layout.add_widget(self.btn_capitulo)
        
        # --- BOTÃO: VERSÍCULO ---
        form_layout.add_widget(self.criar_label_alinhado("Versículo:"))
        self.btn_versiculo = BotaoArredondado(text='-', size_hint=(1, 1), height=ALTURA_BOTAO_FORM, disabled=True, cor_fundo=COR_BOTAO_FORM)
        self.btn_versiculo.bind(on_release=self.abrir_seletor_versiculos)
        form_layout.add_widget(self.btn_versiculo)
        
        # --- BOTÃO: TEMA ---
        form_layout.add_widget(self.criar_label_alinhado("Tema:"))
        self.btn_tema = BotaoArredondado(text='Selecione o Tema', size_hint=(1, 1), height=ALTURA_BOTAO_FORM, cor_fundo=COR_BOTAO_FORM)
        self.btn_tema.bind(on_release=self.abrir_seletor_temas)
        form_layout.add_widget(self.btn_tema)
        
        layout_principal.add_widget(form_layout)
        
        self.lbl_mensagem = Label(text="", size_hint=(1, 0.05))
        layout_principal.add_widget(self.lbl_mensagem)
        
        box_botoes = BoxLayout(orientation='horizontal', spacing=ESPACO_PADRAO, size_hint=(1, ALTURA_FOOTER))
        
        btn_voltar = BotaoArredondado(text="Voltar", cor_fundo=COR_BOTAO_VOLTAR)
        btn_voltar.bind(on_release=self.voltar_home)
        
        btn_salvar = BotaoArredondado(text="Salvar", cor_fundo=COR_BOTAO_SUCESSO)
        btn_salvar.bind(on_release=self.salvar_versiculo)
        
        box_botoes.add_widget(btn_voltar)
        box_botoes.add_widget(btn_salvar)
        
        layout_principal.add_widget(box_botoes)
        self.add_widget(layout_principal)

    def on_pre_enter(self, *args):
        self.lbl_mensagem.text = ""
        
    def criar_label_alinhado(self, texto):
        lbl = Label(
            text=texto, 
            halign="right",       
            valign="middle",      
            size_hint_y=1, 
            #height=ALTURA_BOTAO_FORM, # O Label agora acompanha a variável de altura automaticamente
            padding_x=dp(10)      
        )
        lbl.bind(size=lbl.setter('text_size'))
        return lbl

    # ==========================================
    # LÓGICA DOS SELETORES (ESTILO YOUVERSION)
    # ==========================================

    def abrir_seletor_livros(self, instancia):
        conteudo = ScrollView(size_hint=(1, 1))
        grade = GridLayout(cols=1, spacing=ESPACO_PADRAO, size_hint_y=None, padding=dp(10))
        grade.bind(minimum_height=grade.setter('height'))
        
        livros = self.db.listar_livros()
        popup = Popup(title="Selecione o Livro", content=conteudo, size_hint=(0.9, 0.8))

        def selecionar(btn):
            self.btn_livro.text = btn.text
            popup.dismiss()
            self.btn_capitulo.text = 'Selecione'
            self.btn_capitulo.disabled = False
            self.btn_versiculo.text = '-'
            self.btn_versiculo.disabled = True

        for livro in livros:
            btn = BotaoArredondado(text=livro, size_hint_y=None, height=ALTURA_BOTAO_POPUP, raio=5, cor_fundo=COR_BOTAO_POPUP)
            btn.bind(on_release=selecionar)
            grade.add_widget(btn)

        conteudo.add_widget(grade)
        popup.open()

    def abrir_seletor_capitulos(self, instancia):
        conteudo = ScrollView(size_hint=(1, 1))
        grade = GridLayout(cols=4, spacing=ESPACO_PADRAO, size_hint_y=None, padding=dp(10))
        grade.bind(minimum_height=grade.setter('height'))
        
        capitulos = self.db.listar_capitulos(self.btn_livro.text)
        popup = Popup(title=f"Capítulos de {self.btn_livro.text}", content=conteudo, size_hint=(0.9, 0.8))

        def selecionar(btn):
            self.btn_capitulo.text = btn.text
            popup.dismiss()
            self.btn_versiculo.text = 'Selecione'
            self.btn_versiculo.disabled = False

        for cap in capitulos:
            btn = BotaoArredondado(text=cap, size_hint_y=None, height=ALTURA_BOTAO_POPUP, raio=10, cor_fundo=COR_BOTAO_POPUP)
            btn.bind(on_release=selecionar)
            grade.add_widget(btn)

        conteudo.add_widget(grade)
        popup.open()

    def abrir_seletor_versiculos(self, instancia):
        conteudo = ScrollView(size_hint=(1, 1))
        grade = GridLayout(cols=5, spacing=ESPACO_PADRAO, size_hint_y=None, padding=dp(10))
        grade.bind(minimum_height=grade.setter('height'))
        
        versiculos = self.db.listar_versiculos(self.btn_livro.text, int(self.btn_capitulo.text))
        popup = Popup(title=f"Versículos", content=conteudo, size_hint=(0.9, 0.8))

        def selecionar(btn):
            self.btn_versiculo.text = btn.text
            popup.dismiss()

        for ver in versiculos:
            btn = BotaoArredondado(text=ver, size_hint_y=None, height=ALTURA_BOTAO_POPUP, raio=10, cor_fundo=COR_BOTAO_POPUP)
            btn.bind(on_release=selecionar)
            grade.add_widget(btn)

        conteudo.add_widget(grade)
        popup.open()

    def abrir_seletor_temas(self, instancia):
        # Uma caixa vertical para segurar a lista em cima e o botão embaixo
        box_principal = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(5))
        
        conteudo = ScrollView(size_hint=(1, 1))
        grade = GridLayout(cols=1, spacing=ESPACO_PADRAO, size_hint_y=None, padding=dp(10))
        grade.bind(minimum_height=grade.setter('height'))
        
        temas = self.db.listar_temas()
        popup = Popup(title="Selecione o Tema", content=box_principal, size_hint=(0.9, 0.8))

        def selecionar(btn):
            self.btn_tema.text = btn.text
            popup.dismiss()

        if not temas:
            grade.add_widget(Label(text="Nenhum tema cadastrado ainda.", size_hint_y=None, height=ALTURA_BOTAO_POPUP))
        else:
            for tema in temas:
                # Ajustei a cor para ficar no padrão (azul)
                btn = BotaoArredondado(text=tema['nome_tema'], size_hint_y=None, height=ALTURA_BOTAO_POPUP, raio=5, cor_fundo=COR_BOTAO_POPUP)
                btn.bind(on_release=selecionar)
                grade.add_widget(btn)

        conteudo.add_widget(grade)
        box_principal.add_widget(conteudo)
        
        # --- NOVO BOTÃO: CRIAR TEMA ---
        btn_novo_tema = BotaoArredondado(text="+ Criar Novo Tema", size_hint_y=None, height=dp(50), cor_fundo=COR_BOTAO_SUCESSO)
        
        def chamar_criacao_tema(btn):
            popup.dismiss()           # Fecha a lista
            self.abrir_criacao_tema() # Abre o teclado
            
        btn_novo_tema.bind(on_release=chamar_criacao_tema)
        box_principal.add_widget(btn_novo_tema)
        # ------------------------------
        
        popup.open()
        
    def abrir_criacao_tema(self):
        """Abre um Popup para o usuário criar um tema sem perder o preenchimento do versículo."""
        box_popup = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        input_nome = TextInput(multiline=False, hint_text="Ex: Fé, Esperança...", font_size=dp(18), size_hint_y=0.4)
        box_popup.add_widget(input_nome)
        
        lbl_erro = Label(text="", color=COR_TEXTO_ERRO, size_hint_y=0.2)
        box_popup.add_widget(lbl_erro)
        
        box_botoes = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.4)
        btn_cancelar = BotaoArredondado(text="Cancelar", cor_fundo=COR_BOTAO_VOLTAR)
        btn_salvar = BotaoArredondado(text="Adicionar", cor_fundo=COR_BOTAO_SUCESSO)
        
        box_botoes.add_widget(btn_cancelar)
        box_botoes.add_widget(btn_salvar)
        box_popup.add_widget(box_botoes)
        
        popup = Popup(title="Criar Novo Tema", content=box_popup, size_hint=(0.85, 0.35))
        btn_cancelar.bind(on_release=popup.dismiss)
        
        def salvar_novo_tema(btn):
            nome_novo = input_nome.text.strip().title()
            
            if not nome_novo:
                lbl_erro.text = "O nome não pode estar vazio!"
                return
                
            temas_existentes = self.db.listar_temas()
            for t in temas_existentes:
                if t['nome_tema'].title() == nome_novo:
                    lbl_erro.text = "Este tema já existe!"
                    return 
            
            # 1. Salva o tema no banco de dados
            self.db.obter_ou_criar_tema(nome_novo)
            
            # 2. O Toque de Mestre: já deixa o botão do formulário preenchido com ele!
            self.btn_tema.text = nome_novo
            popup.dismiss()
                
        btn_salvar.bind(on_release=salvar_novo_tema)
        popup.open()

    # ==========================================
    # LÓGICA DE SALVAR
    # ==========================================

    def salvar_versiculo(self, instancia):
        livro = self.btn_livro.text
        capitulo = self.btn_capitulo.text
        versiculo = self.btn_versiculo.text
        tema = self.btn_tema.text 
        
        if livro == 'Selecione o Livro' or capitulo in ('-', 'Selecione') or versiculo in ('-', 'Selecione') or tema == 'Selecione o Tema':
            self.lbl_mensagem.text = "Preencha todos os campos!"
            self.lbl_mensagem.color = COR_TEXTO_ERRO
            return
            
        sucesso, mensagem = self.db.vincular_versiculo_tema(livro, int(capitulo), int(versiculo), tema)
        
        self.lbl_mensagem.text = mensagem
        if sucesso:
            self.lbl_mensagem.color = COR_TEXTO_SUCESSO
            self.btn_versiculo.text = 'Selecione' 
        else:
            self.lbl_mensagem.color = COR_TEXTO_ERRO

    def voltar_home(self, instancia):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'