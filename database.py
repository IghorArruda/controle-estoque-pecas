"""
database.py — Gerenciamento do banco de dados SQLite
============================================
O QUE É:
  Este arquivo cria e gerencia as tabelas do banco de dados.
  É como a "planilha secreta" onde o app guarda tudo.

O QUE VOCÊ FAZ:
  1. Cria um arquivo chamado "database.py" na pasta do projeto
  2. Cola este código inteiro dentro dele
  3. Não precisa alterar nada aqui (só se quiser mudar nomes de tabelas)

COMO FUNCIONA:
  - SQLite = banco de dados leve, não precisa instalar servidor
  - Cria arquivo "estoque.db" na mesma pasta (é o banco de dados)
  - Duas tabelas: "produtos" (catálogo) e "movimentacoes" (histórico)
"""

import sqlite3
from datetime import datetime

# Nome do arquivo do banco de dados (fica na mesma pasta do app)
DB_NAME = "estoque.db"


def conectar():
    """
    O que faz: Abre a conexão com o banco de dados.
    Você não chama isso diretamente, as outras funções chamam.
    """
    return sqlite3.connect(DB_NAME)


def criar_tabelas():
    """
    O que faz: Cria as tabelas se elas não existirem ainda.
    Quando usar: Uma vez, no início do app. O Streamlit chama automaticamente.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de produtos (catálogo de peças)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            modelo_maquina TEXT NOT NULL,
            quantidade INTEGER DEFAULT 0,
            quantidade_minima INTEGER DEFAULT 1,
            categoria TEXT
        )
    """)

    # Tabela de movimentações (histórico de entradas e saídas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,  -- 'entrada' ou 'saida'
            quantidade INTEGER NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    """)

    conn.commit()
    conn.close()


def inserir_produto(nome, modelo_maquina, quantidade, quantidade_minima, categoria):
    """
    O que faz: Adiciona uma nova peça ao estoque.

    Parâmetros (o que você passa):
      nome = "Placa CPU"
      modelo_maquina = "Máquina A"
      quantidade = 2
      quantidade_minima = 2
      categoria = "Eletrônica"
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, modelo_maquina, quantidade, quantidade_minima, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, modelo_maquina, quantidade, quantidade_minima, categoria))
    conn.commit()
    conn.close()


def listar_produtos():
    """
    O que faz: Pega TODAS as peças do estoque.
    Retorna: Lista de tuplas (id, nome, modelo, quantidade, minima, categoria)
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos ORDER BY nome")
    produtos = cursor.fetchall()
    conn.close()
    return produtos


def buscar_produtos(termo):
    """
    O que faz: Procura peças por nome OU modelo da máquina.

    Parâmetro:
      termo = "Placa" ou "Máquina A" (busca parcial, não precisa ser exato)
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM produtos 
        WHERE nome LIKE ? OR modelo_maquina LIKE ?
        ORDER BY nome
    """, (f"%{termo}%", f"%{termo}%"))
    produtos = cursor.fetchall()
    conn.close()
    return produtos


def atualizar_quantidade(produto_id, nova_quantidade, tipo_movimentacao, qtd_movimentada):
    """
    O que faz: Atualiza a quantidade de uma peça E registra no histórico.

    Parâmetros:
      produto_id = ID da peça (número)
      nova_quantidade = quantidade final (ex: 3)
      tipo_movimentacao = "entrada" ou "saida"
      qtd_movimentada = quantidade que entrou/saiu (ex: 1)
    """
    conn = conectar()
    cursor = conn.cursor()

    # Atualiza a quantidade no estoque
    cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, produto_id))

    # Registra a movimentação no histórico
    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, data_hora)
        VALUES (?, ?, ?, ?)
    """, (produto_id, tipo_movimentacao, qtd_movimentada, datetime.now()))

    conn.commit()
    conn.close()


def excluir_produto(produto_id):
    """
    O que faz: Remove uma peça do estoque completamente.
    Atenção: Também apaga o histórico dessa peça (por causa do FOREIGN KEY).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movimentacoes WHERE produto_id = ?", (produto_id,))
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()


def listar_movimentacoes(produto_id=None, limite=100):
    """
    O que faz: Mostra o histórico de movimentações.

    Parâmetros:
      produto_id = filtra por uma peça específica (ou None para todas)
      limite = quantos registros mostrar (padrão: 100 últimos)
    """
    conn = conectar()
    cursor = conn.cursor()

    if produto_id:
        cursor.execute("""
            SELECT m.*, p.nome 
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            WHERE m.produto_id = ?
            ORDER BY m.data_hora DESC
            LIMIT ?
        """, (produto_id, limite))
    else:
        cursor.execute("""
            SELECT m.*, p.nome 
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            ORDER BY m.data_hora DESC
            LIMIT ?
        """, (limite,))

    movimentacoes = cursor.fetchall()
    conn.close()
    return movimentacoes


def produtos_baixo_estoque():
    """
    O que faz: Lista todas as peças com quantidade ABAIXO do mínimo.
    Retorna: Lista de produtos em alerta (para mostrar em vermelho no app)
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM produtos 
        WHERE quantidade <= quantidade_minima
        ORDER BY quantidade ASC
    """)
    produtos = cursor.fetchall()
    conn.close()
    return produtos
