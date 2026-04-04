from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from views.componentes import BotaoArredondado

from models.database import BancoDeDados

ALTURA_BOTAO_FORM = dp(60) 
ALTURA_BOTAO_POPUP = dp(60)
ESPACO_PADRAO = dp(10)

COR_BOTAO_FORM = (0.3, 0.3, 0.3, 1)       # Cinza escuro
COR_BOTAO_POPUP = (0.2, 0.5, 0.8, 1)      # Azul
COR_BOTAO_SUCESSO = (0.2, 0.7, 0.3, 1)    # Verde
COR_BOTAO_VOLTAR = (0.4, 0.4, 0.4, 1)     # Cinza médio
COR_TEXTO_ERRO = (1, 0.3, 0.3, 1)         # Vermelho
COR_TEXTO_SUCESSO = (0.3, 1, 0.3, 1)      # Verde claro
COR_BOTAO_EXLCUIR = (0.8, 0.2, 0.2, 1)

ALTURA_TITULO = 0.15
ALTURA_TABELA = 0.65
ALTURA_FOOTER = 0.20

class TemasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = BancoDeDados()
        
        # Layout Principal
        self.layout_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Cabeçalho
        self.layout_principal.add_widget(Label(text="Meus Temas", font_size=dp(28), size_hint=(1, ALTURA_TITULO), bold=True))
        
        # Área de Rolagem (ScrollView)
        self.scroll = ScrollView(size_hint=(1, ALTURA_TABELA))
        
        # A grade interna que vai crescer conforme o número de temas
        self.grade_temas = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.grade_temas.bind(minimum_height=self.grade_temas.setter('height'))
        
        self.scroll.add_widget(self.grade_temas)
        self.layout_principal.add_widget(self.scroll)
        
        # Botões do Rodapé
        box_botoes = BoxLayout(orientation='horizontal', spacing=ESPACO_PADRAO, size_hint=(1, ALTURA_FOOTER))
        
        btn_voltar = BotaoArredondado(text="Voltar", cor_fundo=COR_BOTAO_VOLTAR)
        btn_voltar.bind(on_release=self.voltar_home)
        
        btn_add_tema = BotaoArredondado(text="Adicionar Tema", cor_fundo=COR_BOTAO_SUCESSO)
        btn_add_tema.bind(on_release=self.criar_tema)
        
        box_botoes.add_widget(btn_voltar)
        box_botoes.add_widget(btn_add_tema)
        
        self.layout_principal.add_widget(box_botoes)
        
        self.add_widget(self.layout_principal)

    def on_pre_enter(self, *args):
        """Executa toda vez que a tela está prestes a aparecer."""
        self.carregar_temas()

    def carregar_temas(self):
        self.grade_temas.clear_widgets() 
        temas = self.db.listar_temas()
        
        if not temas:
            self.grade_temas.add_widget(Label(text="Nenhum tema cadastrado.", size_hint_y=None, height=dp(50)))
            return
            
        for tema in temas:
            nome_tema = tema['nome_tema']
            quantidade = tema['qtd']
            
            linha = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), spacing=dp(5))
            
            # --- ÁREA DO TEMA (USANDO MARKUP) ---
            # Tags do Kivy: [b] negrito, [size] tamanho, [color] cor hexadecimal
            texto_formatado = f"[b]{nome_tema}[/b]\n[size=13dp][color=#cccccc]Qtd: {quantidade}[/color][/size]"
            
            btn_tema = BotaoArredondado(
                text=texto_formatado,
                markup=True,           # LIGA O TEXTO RICO!
                size_hint_x=0.66, 
                cor_fundo=COR_BOTAO_POPUP,
                halign='center',         # Alinha à esquerda
                valign='middle',       # Centraliza na vertical
                padding=(dp(15), dp(0))# Dá um respiro da borda esquerda
            )
            # Amarra o tamanho do texto ao botão para o halign='left' funcionar
            btn_tema.bind(size=btn_tema.setter('text_size'))
            btn_tema.bind(on_release=lambda btn, n=nome_tema: self.abrir_detalhes_por_nome(n))
            
            # --- BOTÕES DE AÇÃO (ÍCONES) ---
            btn_editar = BotaoArredondado(
                text=u'\U000f03eb', 
                font_name='MDI',
                size_hint_x=0.17, 
                font_size=dp(22), 
                cor_fundo=(0.3, 0.3, 0.3, 1), 
                raio=5
            )
            btn_editar.bind(on_release=lambda btn, n=nome_tema: self.popup_editar_tema(n))
            
            btn_excluir = BotaoArredondado(
                text="X", 
                size_hint_x=0.17, 
                font_size=dp(18), 
                cor_fundo=(0.8, 0.2, 0.2, 1), 
                raio=5
            )
            btn_excluir.bind(on_release=lambda btn, n=nome_tema: self.confirmar_exclusao(n))
            
            linha.add_widget(btn_tema)
            linha.add_widget(btn_editar)
            linha.add_widget(btn_excluir)
            
            self.grade_temas.add_widget(linha)

    def abrir_detalhes_por_nome(self, nome_tema):
        """Método auxiliar para disparar a navegação pelo nome capturado no loop."""
        tela_detalhe = self.manager.get_screen('tema_detalhe')
        tela_detalhe.tema_atual = nome_tema
        self.manager.transition.direction = 'left' 
        self.manager.current = 'tema_detalhe'

    def popup_editar_tema(self, nome_antigo):
        """Abre popup para renomear o tema com as mesmas validações de criação."""
        box = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        input_nome = TextInput(text=nome_antigo, multiline=False, font_size=dp(18), size_hint_y=0.4)
        lbl_erro = Label(text="", color=COR_TEXTO_ERRO, size_hint_y=0.2)
        
        box_btn = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.4)
        btn_can = BotaoArredondado(text="Cancelar", cor_fundo=COR_BOTAO_VOLTAR)
        btn_sal = BotaoArredondado(text="Salvar", cor_fundo=COR_BOTAO_SUCESSO)
        
        box.add_widget(input_nome)
        box.add_widget(lbl_erro)
        box_btn.add_widget(btn_can)
        box_btn.add_widget(btn_sal)
        box.add_widget(box_btn)
        
        popup = Popup(title=f"Editar Tema: {nome_antigo}", content=box, size_hint=(0.85, 0.35))
        btn_can.bind(on_release=popup.dismiss)
        
        def salvar_edicao(btn):
            novo_nome = input_nome.text.strip().title()
            if not novo_nome:
                lbl_erro.text = "O nome não pode estar vazio!"
                return
            
            if novo_nome == nome_antigo.title():
                popup.dismiss()
                return

            # Validação de duplicata com o novo padrão
            temas = self.db.listar_temas()
            if any(t['nome_tema'].title() == novo_nome for t in temas):
                lbl_erro.text = "Este nome de tema já existe!"
                return

            self.db.atualizar_nome_tema(nome_antigo, novo_nome)
            self.carregar_temas()
            popup.dismiss()

        btn_sal.bind(on_release=salvar_edicao)
        popup.open()

    def confirmar_exclusao(self, nome_tema):
        """Popup de segurança para evitar exclusão acidental."""
        box = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        lbl_aviso = Label(
            text=f"Deseja excluir o tema '{nome_tema}'?\nIsso removerá todos os versículos vinculados!", 
            halign="center",
            valign="middle"
        )
        lbl_aviso.bind(size=lbl_aviso.setter('text_size')) 
        box.add_widget(lbl_aviso)
        
        #---------------------------
        
        box_btn = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.4)
        btn_can = BotaoArredondado(text="Não", cor_fundo=COR_BOTAO_VOLTAR)
        btn_sim = BotaoArredondado(text="Sim, Excluir", cor_fundo=COR_BOTAO_EXLCUIR)
        
        #---------------------------
        
        box_btn.add_widget(btn_can)
        box_btn.add_widget(btn_sim)
        box.add_widget(box_btn)
        
        popup = Popup(title="Confirmar Exclusão", content=box, size_hint=(0.8, 0.4))
        btn_can.bind(on_release=popup.dismiss)
        
        def deletar(btn):
            self.db.excluir_tema(nome_tema)
            self.carregar_temas()
            popup.dismiss()
            
        btn_sim.bind(on_release=deletar)
        popup.open()

    def voltar_home(self, instancia):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
        
    def criar_tema(self, instancia):
        """Abre um Popup para digitar e validar o novo tema."""
        box_popup = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Campo de entrada de texto
        input_nome = TextInput(multiline=False, hint_text="Ex: Fé, Esperança...", font_size=dp(18), size_hint_y=0.4)
        box_popup.add_widget(input_nome)
        
        # Label para exibir erros de validação
        lbl_erro = Label(text="", color=COR_TEXTO_ERRO, size_hint_y=0.2)
        box_popup.add_widget(lbl_erro)
        
        # Botões do Popup
        box_botoes = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.4)
        btn_cancelar = BotaoArredondado(text="Cancelar", cor_fundo=COR_BOTAO_VOLTAR)
        btn_salvar = BotaoArredondado(text="Adicionar", cor_fundo=COR_BOTAO_SUCESSO)
        
        box_botoes.add_widget(btn_cancelar)
        box_botoes.add_widget(btn_salvar)
        box_popup.add_widget(box_botoes)
        
        popup = Popup(title="Criar Novo Tema", content=box_popup, size_hint=(0.85, 0.35))
        
        btn_cancelar.bind(on_release=popup.dismiss)
        
        # Lógica de Validação e Salvamento
        def salvar_novo_tema(btn):
            # 1. Remove espaços em branco nas pontas
            nome_novo = input_nome.text.strip().title()
            
            # 2. Verifica se está vazio
            if not nome_novo:
                lbl_erro.text = "O nome não pode estar vazio!"
                return
                
            # 3. Busca temas existentes e verifica duplicatas ignorando maiúsculas/minúsculas
            temas_existentes = self.db.listar_temas()
            
            for t in temas_existentes:
                if t['nome_tema'].title() == nome_novo:
                    lbl_erro.text = "Este tema já existe!"
                    return
            
            # 4. Se passou por todas as travas, salva no banco (mantendo a formatação original)
            self.db.obter_ou_criar_tema(nome_novo)
            
            self.carregar_temas() # Atualiza a lista na tela principal
            popup.dismiss()       # Fecha a janelinha
                
        btn_salvar.bind(on_release=salvar_novo_tema)
        popup.open()
        
    def abrir_detalhes(self, instancia):
        nome_do_tema_clicado = instancia.text
        tela_detalhe = self.manager.get_screen('tema_detalhe')
        tela_detalhe.tema_atual = nome_do_tema_clicado
        self.manager.transition.direction = 'left' 
        self.manager.current = 'tema_detalhe'