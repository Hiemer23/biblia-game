# 📖 Setup: Como rodar o MemoBíblia em um PC Novo

Este guia contém o passo a passo para baixar, configurar e rodar o aplicativo do zero em qualquer computador.

## ⚠️ Pré-requisito Crucial
Para evitar erros de compilação do Kivy (especialmente no Windows), **NÃO** utilize versões do Python em fase de testes (como 3.13 ou 3.14). 
Certifique-se de ter o **Python 3.11 ou 3.12** instalado na máquina.

---

## Passo 1: Baixar o Código
Abra o terminal e clone o repositório do GitHub:
```bash
git clone https://github.com/Hiemer23/biblia-game.git
cd biblia-game
```

## Passo 2: Garantir que esteja em uma versão estável do python
Atualmente a versão estável é 3.12
```bash
py install 3.12
```

## Passo 2: Criar e Ativar o Ambiente Virtual

Nunca instale as dependências globalmente. Crie um ambiente isolado (venv).

### No Windows (PowerShell):
```
py -3.12 -m venv .venv
.\.venv\Scripts\activate
```

(Se der erro de permissão no Windows, rode Set-ExecutionPolicy RemoteSigned -Scope CurrentUser e tente ativar novamente).

### No Linux / Mac:
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```
O ambiente estará ativo quando aparecer (.venv) no início da linha do terminal.
## Passo 3: Instalar as Dependências

Com o ambiente ativado, instale o Kivy e outras bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

## Passo 4: Rodar o Aplicativo

Com as bibliotecas instaladas e o banco de dados populado, basta dar o play:
```bash
python main.py
```