import sqlite3
import os

def configurar_banco():
    
    # 1. Resolve o problema da pasta: cria a pasta 'db' se ela não existir
    pasta_db = '../db'
    os.makedirs(pasta_db, exist_ok=True)
    
    # Caminho correto para Linux/Mac/Termux
    caminho_banco = os.path.join(pasta_db, 'memobiblia.db')

    # Conecta ao banco na pasta correta
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    
    print(f"Limpando e recriando o banco de dados em: {caminho_banco}...")

    # 2. O RESET ABSOLUTO: Destrói as tabelas velhas se elas existirem
    cursor.execute('DROP TABLE IF EXISTS memorizacao')
    cursor.execute('DROP TABLE IF EXISTS temas')
    cursor.execute('DROP TABLE IF EXISTS textos_biblicos')

    # 3. Recria as tabelas 100% limpas e vazias
    cursor.execute('''
        CREATE TABLE textos_biblicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro TEXT NOT NULL,
            capitulo INTEGER NOT NULL,
            versiculo INTEGER NOT NULL,
            texto TEXT NOT NULL,
            versao TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE temas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_tema TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE memorizacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto_id INTEGER,
            tema_id INTEGER,
            acertos INTEGER DEFAULT 0,
            erros INTEGER DEFAULT 0,
            FOREIGN KEY (texto_id) REFERENCES textos_biblicos (id),
            FOREIGN KEY (tema_id) REFERENCES temas (id)
        )
    ''')

    # Salva e fecha a porta
    conexao.commit()
    conexao.close()
    print("Sucesso! Banco de dados zerado e estruturado na pasta 'db'.")

if __name__ == '__main__':
    configurar_banco()