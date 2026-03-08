import sqlite3
import os
import json

def popular_temas_iniciais():
    # 1. Configura os caminhos absolutos para a base de dados e para o JSON
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_db = os.path.abspath(os.path.join(diretorio_atual, '..', 'db', 'memobiblia.db'))
    caminho_json = os.path.join(diretorio_atual, 'temas_iniciais.json')

    # 2. Lê o ficheiro JSON
    try:
        with open(caminho_json, 'r', encoding='utf-8') as ficheiro:
            temas_iniciais = json.load(ficheiro)
    except FileNotFoundError:
        print(f"Erro: Ficheiro {caminho_json} não encontrado.")
        return

    # 3. Liga à base de dados
    conexao = sqlite3.connect(caminho_db)
    cursor = conexao.cursor()

    print(f"A ler dados de: {caminho_json}")
    print("A iniciar o seed de temas e versículos...\n")

    # 4. Processa o dicionário gerado pelo JSON
    for nome_tema, lista_versiculos in temas_iniciais.items():
        cursor.execute('INSERT OR IGNORE INTO temas (nome_tema) VALUES (?)', (nome_tema,))
        
        cursor.execute('SELECT id FROM temas WHERE nome_tema = ?', (nome_tema,))
        tema_id = cursor.fetchone()[0]
        print(f"Tema '{nome_tema}' (ID: {tema_id}) pronto.")

        # Agora usamos as coordenadas puras em vez do texto_id
        for ref in lista_versiculos:
            livro = ref['livro']
            capitulo = ref['capitulo']
            versiculo = ref['versiculo']

            # Verifica se esta coordenada exata já está associada a este tema
            cursor.execute('''
                SELECT id FROM memorizacao 
                WHERE livro = ? AND capitulo = ? AND versiculo = ? AND tema_id = ?
            ''', (livro, capitulo, versiculo, tema_id))
            
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO memorizacao (livro, capitulo, versiculo, tema_id, acertos, erros)
                    VALUES (?, ?, ?, ?, 0, 0)
                ''', (livro, capitulo, versiculo, tema_id))
                print(f"  -> [Vinculado] {livro} {capitulo}:{versiculo}")
            else:
                print(f"  -> [Aviso] {livro} {capitulo}:{versiculo} já estava vinculado.")

    conexao.commit()
    conexao.close()
    print("\nSeed concluído com sucesso! Os jogos já têm dados limpos para carregar.")

if __name__ == '__main__':
    popular_temas_iniciais()