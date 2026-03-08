import sqlite3

def importar_biblia(arquivo_origem, arquivo_destino, sigla_versao):
    print(f"Iniciando a importação da versão {sigla_versao}...")
    
    # Conecta aos dois bancos de dados
    con_origem = sqlite3.connect(arquivo_origem)
    cur_origem = con_origem.cursor()
    
    con_destino = sqlite3.connect(arquivo_destino)
    cur_destino = con_destino.cursor()
    
    # Faz um SELECT na origem juntando a tabela 'verse' com a tabela 'book'
    query_origem = '''
        SELECT b.name, v.chapter, v.verse, v.text
        FROM verse v
        JOIN book b ON v.book_id = b.id
    '''
    cur_origem.execute(query_origem)
    versiculos_origem = cur_origem.fetchall()
    
    print(f"Encontrados {len(versiculos_origem)} versículos. Preparando para salvar...")
    
    # Monta a lista no formato exato da nossa tabela textos_biblicos
    dados_para_inserir = []
    for linha in versiculos_origem:
        livro = linha[0]
        capitulo = linha[1]
        versiculo = linha[2]
        texto = linha[3]
        # Adiciona a sigla da versão no final da tupla
        dados_para_inserir.append((livro, capitulo, versiculo, texto, sigla_versao))
        
    # Limpa dados antigos dessa mesma versão para não duplicar se você rodar o script duas vezes
    cur_destino.execute('DELETE FROM textos_biblicos WHERE versao = ?', (sigla_versao,))
    
    # Injeta todos os milhares de versículos de uma só vez na nossa tabela
    query_destino = '''
        INSERT INTO textos_biblicos (livro, capitulo, versiculo, texto, versao)
        VALUES (?, ?, ?, ?, ?)
    '''
    cur_destino.executemany(query_destino, dados_para_inserir)
    
    # Salva e fecha as conexões
    con_destino.commit()
    con_origem.close()
    con_destino.close()
    
    print(f"Sucesso! Todos os versículos da {sigla_versao} foram importados para o memobiblia.db.")

if __name__ == '__main__':
    # Executa a função apontando para os arquivos corretos
    importar_biblia('../biblias/NVI.sqlite', '../db/memobiblia.db', 'NVI')