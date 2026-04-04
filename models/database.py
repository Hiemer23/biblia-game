import sqlite3
import os

class BancoDeDados:
    def __init__(self):
        # 1. Descobre a pasta exata onde este arquivo (database.py) está salvo
        diretorio_deste_arquivo = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Constrói o caminho: vai para a pasta do arquivo -> sobe um nível (..) -> entra em 'db' -> 'memobiblia.db'
        caminho_sujo = os.path.join(diretorio_deste_arquivo, '..', 'db', 'memobiblia.db')
        
        # 3. Limpa o caminho (transforma /models/../db/ em /db/)
        self.caminho_db = os.path.abspath(caminho_sujo)

    def _conectar(self):
        """Cria e retorna uma conexão com o banco de dados."""
        conexao = sqlite3.connect(self.caminho_db)
        
        # O Pulo do Gato: Isso faz o SQLite retornar dicionários em vez de tuplas.
        # Assim você pode usar linha['texto'] em vez de tentar adivinhar que era a linha[3].
        conexao.row_factory = sqlite3.Row 
        return conexao

    def buscar_versiculo_especifico(self, livro, capitulo, versiculo, versao="AS21"):
        """Busca um único versículo no banco."""
        query = """
            SELECT texto FROM textos_biblicos 
            WHERE livro = ? AND capitulo = ? AND versiculo = ? AND versao = ?
        """
        # O 'with' garante que a conexão será fechada automaticamente após o uso
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (livro, capitulo, versiculo, versao))
            resultado = cursor.fetchone()
            
            if resultado:
                return resultado['texto']
            return "Versículo não encontrado."

    def buscar_capitulo_inteiro(self, livro, capitulo, versao="AS21"):
        """Retorna uma lista com todos os versículos de um capítulo."""
        query = """
            SELECT versiculo, texto FROM textos_biblicos 
            WHERE livro = ? AND capitulo = ? AND versao = ?
            ORDER BY versiculo ASC
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (livro, capitulo, versao))
            # Retorna uma lista de dicionários
            return [dict(linha) for linha in cursor.fetchall()]

    def obter_ou_criar_tema(self, nome_tema):
        """Busca o ID de um tema. Se ele não existir, cria na hora."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            # Tenta buscar primeiro
            cursor.execute("SELECT id FROM temas WHERE nome_tema = ?", (nome_tema,))
            resultado = cursor.fetchone()
            
            if resultado:
                return resultado['id']
            
            # Se não existe, cria o tema novo e retorna o ID dele
            cursor.execute("INSERT INTO temas (nome_tema) VALUES (?)", (nome_tema,))
            conn.commit()
            return cursor.lastrowid

    def vincular_versiculo_tema(self, livro, capitulo, versiculo, nome_tema):
        """Salva a coordenada pura do versículo ligada ao tema."""
        try:
            # Garante que o tema existe e pega o ID (com a nossa formatação .title() se vier da tela)
            tema_id = self.obter_ou_criar_tema(nome_tema)

            with self._conectar() as conn:
                cursor = conn.cursor()
                
                # A sua trava original impecável
                cursor.execute("""
                    SELECT id FROM memorizacao 
                    WHERE livro = ? AND capitulo = ? AND versiculo = ? AND tema_id = ?
                """, (livro, capitulo, versiculo, tema_id))
                
                if cursor.fetchone():
                    return False, f"O versículo já está cadastrado em {nome_tema}."

                # O seu INSERT original com as colunas de acertos e erros
                cursor.execute("""
                    INSERT INTO memorizacao (livro, capitulo, versiculo, tema_id, acertos, erros)
                    VALUES (?, ?, ?, ?, 0, 0)
                """, (livro, capitulo, versiculo, tema_id))
                
                conn.commit()
                return True, "Versículo adicionado com sucesso!"
                
        except Exception as e:
            return False, f"Erro no banco: {str(e)}"

    def remover_vinculo_tema(self, livro, capitulo, versiculo, nome_tema):
        """Remove um versículo de um tema específico (Delete) pelas coordenadas."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Pega o ID do tema primeiro
            cursor.execute("SELECT id FROM temas WHERE nome_tema = ?", (nome_tema,))
            tema = cursor.fetchone()
            
            if not tema:
                return False, "Tema não encontrado."
                
            # Deleta o vínculo usando as coordenadas
            cursor.execute("""
                DELETE FROM memorizacao 
                WHERE livro = ? AND capitulo = ? AND versiculo = ? AND tema_id = ?
            """, (livro, capitulo, versiculo, tema['id']))
            conn.commit()
            
            return True, "Versículo removido do tema."

    
    def listar_livros(self):
        """Retorna todos os livros na ordem bíblica correta."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            # Agrupa pelo nome, mas ordena pelo ID mínimo para manter Gênesis primeiro e Apocalipse por último
            cursor.execute("SELECT livro FROM textos_biblicos GROUP BY livro ORDER BY min(id)")
            return [linha['livro'] for linha in cursor.fetchall()]

    def listar_capitulos(self, livro):
        """Retorna os capítulos disponíveis de um livro específico."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT capitulo FROM textos_biblicos WHERE livro = ? ORDER BY capitulo", (livro,))
            return [str(linha['capitulo']) for linha in cursor.fetchall()]

    def listar_versiculos(self, livro, capitulo):
        """Retorna os versículos de um capítulo específico."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT versiculo FROM textos_biblicos WHERE livro = ? AND capitulo = ? ORDER BY versiculo", (livro, capitulo))
            return [str(linha['versiculo']) for linha in cursor.fetchall()]
    
    def listar_temas(self):
        """Retorna a lista de temas e a quantidade de versículos em cada um."""
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Usamos um sub-select para contar os versículos vinculados a cada ID de tema
            cursor.execute("""
                SELECT id, nome_tema, 
                (SELECT COUNT(*) FROM memorizacao WHERE tema_id = temas.id) as qtd 
                FROM temas 
                ORDER BY nome_tema ASC
            """)
            return [dict(row) for row in cursor.fetchall()]
        
    def listar_versiculos_do_tema(self, nome_tema, versao="AS21"):
        """Retorna as coordenadas e o TEXTO dos versículos vinculados a um tema."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            # Fazemos um JOIN duplo: liga a memorização ao tema, e depois ao texto da Bíblia
            cursor.execute("""
                SELECT m.livro, m.capitulo, m.versiculo, b.texto
                FROM memorizacao m
                JOIN temas t ON m.tema_id = t.id
                JOIN textos_biblicos b ON m.livro = b.livro AND m.capitulo = b.capitulo AND m.versiculo = b.versiculo
                WHERE t.nome_tema = ? AND b.versao = ?
                ORDER BY m.livro, m.capitulo, m.versiculo
            """, (nome_tema, versao))
            return [dict(linha) for linha in cursor.fetchall()]
        
    def atualizar_nome_tema(self, nome_antigo, nome_novo):
        """Altera o nome de um tema existente."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE temas SET nome_tema = ? WHERE nome_tema = ?", (nome_novo, nome_antigo))
            conn.commit()

    def excluir_tema(self, nome_tema):
        """Remove um tema e todos os vínculos de versículos associados a ele."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            # 1. Primeiro removemos os versículos da tabela de memorização vinculados a este tema
            cursor.execute("""
                DELETE FROM memorizacao 
                WHERE tema_id = (SELECT id FROM temas WHERE nome_tema = ?)
            """, (nome_tema,))
            
            # 2. Depois removemos o tema em si
            cursor.execute("DELETE FROM temas WHERE nome_tema = ?", (nome_tema,))
            conn.commit()