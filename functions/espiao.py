
import sqlite3

def investigar_banco(arquivo_biblia):
    try:
        conexao = sqlite3.connect(arquivo_biblia)
        cursor = conexao.cursor()
        
        print(f"\n🔍 Investigando o arquivo: {arquivo_biblia}")
        print("="*40)
        
        # Pega o nome de todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        
        for tabela in tabelas:
            nome_tabela = tabela[0]
            print(f"\n📋 Tabela encontrada: {nome_tabela}")
            
            # Pega o nome das colunas de cada tabela
            cursor.execute(f"PRAGMA table_info({nome_tabela})")
            colunas = cursor.fetchall()
            for coluna in colunas:
                nome_coluna = coluna[1]
                tipo_coluna = coluna[2]
                print(f"   ↳ Coluna: {nome_coluna} | Tipo: {tipo_coluna}")
                
        conexao.close()
        print("\n" + "="*40)
    except Exception as e:
        print(f"Erro ao ler o banco: {e}")

if __name__ == '__main__':
    # SUBSTITUA 'ara.sqlite' PELO NOME EXATO DO ARQUIVO QUE VOCÊ BAIXOU DO GITHUB
    investigar_banco('AS21.sqlite')