from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

class BotaoArredondado(Button):
    # Definimos uma cor padrão (Azul) e um arredondamento padrão de 15dp
    def __init__(self, cor_fundo=(0.2, 0.5, 0.8, 1), raio=15, **kwargs):
        super().__init__(**kwargs)
        self.cor_fundo = cor_fundo
        
        # 1. Deixa o botão quadrado original 100% invisível
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.background_down = ''
        
        # 2. Desenha o nosso formato arredondado por trás do texto
        with self.canvas.before:
            self.cor_desenho = Color(*self.cor_fundo)
            # O radius recebe uma lista [raio], que arredonda os 4 cantos iguais
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(raio)])
            
        # 3. Garante que o desenho acompanhe o botão se a tela redimensionar
        self.bind(pos=self.atualizar_shape, size=self.atualizar_shape)
        
    def atualizar_shape(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    # --- EFEITO DE CLIQUE (Feedback Visual) ---
    def on_press(self):
        # Multiplica o RGB por 0.7 para "escurecer" a cor na hora do clique
        self.cor_desenho.rgba = (
            self.cor_fundo[0] * 0.7, 
            self.cor_fundo[1] * 0.7, 
            self.cor_fundo[2] * 0.7, 
            self.cor_fundo[3]
        )
        
    def on_release(self):
        # Volta para a cor original quando solta o dedo
        self.cor_desenho.rgba = self.cor_fundo