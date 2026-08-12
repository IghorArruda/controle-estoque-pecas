"""
app.py — Interface do Aplicativo (Streamlit)
============================================
O QUE É:
  Este arquivo é o "rostinho" do app. Tudo que você vê na tela do celular
  vem daqui: botões, formulários, listas, alertas, gráficos.

O QUE VOCÊ FAZ:
  1. Cria um arquivo chamado "app.py" na pasta do projeto
  2. Cola este código inteiro dentro dele
  3. Para rodar: abre o terminal e digita → streamlit run app.py

COMO FUNCIONA:
  - Streamlit transforma código Python em página web automaticamente
  - Roda no navegador do celular (Chrome, Safari)
  - Interface otimizada para tela pequena (mobile-first)
"""

import streamlit as st
import pandas as pd
from database import (
    criar_tabelas, inserir_produto, listar_produtos, buscar_produtos,
    atualizar_quantidade, excluir_produto, listar_movimentacoes,
    produtos_baixo_estoque
)

# ============================================
# CONFIGURAÇÃO DA PÁGINA (aparencia)
# ============================================
st.set_page_config(
    page_title="Controle de Peças",
    page_icon="🔧",
    layout="centered",  # "centered" = melhor para celular
    initial_sidebar_state="collapsed"  # esconde menu lateral no celular
)

# Cria as tabelas do banco se não existirem
criar_tabelas()

# ============================================
# ESTILO CSS (deixa bonito no celular)
# ============================================
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
    }
    .alerta-estoque {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #ff0000;
    }
    .info-card {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# CABEÇALHO DO APP
# ============================================
st.title("🔧 Controle de Peças")
st.caption("Estoque pessoal de manutenção — Máquinas de Café")

# ============================================
# MENU DE NAVEGAÇÃO (abas no topo)
# ============================================
# O que é: 4 abas que você toca para mudar de tela
# Para que serve: Organiza o app em partes (não fica tudo em uma tela só)
aba = st.tabs(["📦 Estoque", "➕ Entrada", "➖ Saída", "📊 Histórico"])

# ============================================
# ABA 1: ESTOQUE (lista de peças + alertas)
# ============================================
with aba[0]:
    st.subheader("📦 Meu Estoque")

    # Campo de busca (por nome ou modelo da máquina)
    termo_busca = st.text_input("🔍 Buscar peça ou modelo", placeholder="Ex: Placa CPU ou Máquina A")

    # Busca ou lista tudo
    if termo_busca:
        produtos = buscar_produtos(termo_busca)
    else:
        produtos = listar_produtos()

    # ALERTAS: peças com estoque baixo (em vermelho no topo)
    alertas = produtos_baixo_estoque()
    if alertas:
        st.markdown("<div class='alerta-estoque'>", unsafe_allow_html=True)
        st.error(f"⚠️ {len(alertas)} peça(s) com estoque BAIXO!")
        for p in alertas:
            st.write(f"🔴 **{p[1]}** — {p[3]} unid. (mínimo: {p[4]})")
        st.markdown("</div>", unsafe_allow_html=True)

    # Lista de peças (cada peça vira um "card" na tela)
    if produtos:
        for p in produtos:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div class='info-card'>
                        <b>{p[1]}</b> | {p[2]}<br>
                        <span style='font-size: 20px;'>📦 {p[3]} unid.</span> 
                        <span style='font-size: 12px; color: gray;'>(mín: {p[4]})</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    # Botão "-1" para saída rápida (1 toque!)
                    if st.button("➖1", key=f"saida_{p[0]}"):
                        if p[3] > 0:
                            nova_qtd = p[3] - 1
                            atualizar_quantidade(p[0], nova_qtd, "saida", 1)
                            st.success(f"✅ {p[1]}: {p[3]} → {nova_qtd}")
                            st.rerun()
                        else:
                            st.error("❌ Estoque zerado!")
    else:
        st.info("Nenhuma peça encontrada. Cadastre na aba 'Entrada'.")

# ============================================
# ABA 2: ENTRADA (adicionar peças ao estoque)
# ============================================
with aba[1]:
    st.subheader("➕ Entrada de Peças")

    st.markdown("---")
    st.write("**Cadastrar nova peça no estoque:**")

    # Formulário para cadastrar peça nova
    with st.form("cadastro_produto"):
        nome = st.text_input("Nome da peça", placeholder="Ex: Placa CPU")
        modelo = st.selectbox(
            "Modelo da máquina",
            ["Máquina A", "Máquina B", "Máquina C", "Máquina D", "Outro"]
        )
        if modelo == "Outro":
            modelo = st.text_input("Digite o modelo")

        qtd_inicial = st.number_input("Quantidade inicial", min_value=0, value=1, step=1)
        qtd_minima = st.number_input("Quantidade mínima (alerta)", min_value=1, value=2, step=1)
        categoria = st.selectbox(
            "Categoria",
            ["Eletrônica", "Hidráulica", "Mecânica", "Vedação", "Térmica", "Elétrica", "Outro"]
        )

        submit = st.form_submit_button("💾 CADASTRAR PEÇA", use_container_width=True)

        if submit:
            if nome and modelo:
                inserir_produto(nome, modelo, qtd_inicial, qtd_minima, categoria)
                st.success(f"✅ {nome} cadastrado com sucesso!")
                st.balloons()
            else:
                st.error("❌ Preencha nome e modelo!")

    st.markdown("---")
    st.write("**Adicionar quantidade a peça existente:**")

    # Adicionar mais unidades a peça já cadastrada
    produtos_lista = listar_produtos()
    if produtos_lista:
        nomes = [f"{p[1]} ({p[2]}) — {p[3]} unid." for p in produtos_lista]
        selecionado = st.selectbox("Selecione a peça", nomes)
        idx = nomes.index(selecionado)
        produto = produtos_lista[idx]

        qtd_add = st.number_input("Quantidade a adicionar", min_value=1, value=1, step=1)

        if st.button("➕ ADICIONAR AO ESTOQUE", use_container_width=True):
            nova_qtd = produto[3] + qtd_add
            atualizar_quantidade(produto[0], nova_qtd, "entrada", qtd_add)
            st.success(f"✅ {produto[1]}: {produto[3]} → {nova_qtd}")
            st.rerun()
    else:
        st.info("Cadastre uma peça primeiro.")

# ============================================
# ABA 3: SAÍDA (registrar uso de peças)
# ============================================
with aba[2]:
    st.subheader("➖ Saída de Peças")

    produtos_lista = listar_produtos()
    if produtos_lista:
        nomes = [f"{p[1]} ({p[2]}) — {p[3]} unid." for p in produtos_lista]
        selecionado = st.selectbox("Selecione a peça usada", nomes)
        idx = nomes.index(selecionado)
        produto = produtos_lista[idx]

        st.info(f"Estoque atual: **{produto[3]} unid.**")

        qtd_saida = st.number_input("Quantidade usada", min_value=1, max_value=produto[3], value=1, step=1)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➖ CONFIRMAR SAÍDA", use_container_width=True):
                if qtd_saida <= produto[3]:
                    nova_qtd = produto[3] - qtd_saida
                    atualizar_quantidade(produto[0], nova_qtd, "saida", qtd_saida)
                    st.success(f"✅ {produto[1]}: {produto[3]} → {nova_qtd}")
                    st.rerun()
                else:
                    st.error("❌ Quantidade maior que o estoque!")

        with col2:
            # Botão de emergência: excluir peça completamente
            if st.button("🗑️ EXCLUIR PEÇA", use_container_width=True):
                excluir_produto(produto[0])
                st.warning(f"⚠️ {produto[1]} removido do estoque.")
                st.rerun()
    else:
        st.info("Nenhuma peça cadastrada.")

# ============================================
# ABA 4: HISTÓRICO (movimentações)
# ============================================
with aba[3]:
    st.subheader("📊 Histórico de Movimentações")

    # Filtro por peça (ou todas)
    produtos_lista = listar_produtos()
    if produtos_lista:
        opcoes = ["Todas as peças"] + [f"{p[1]} ({p[2]})" for p in produtos_lista]
        filtro = st.selectbox("Filtrar por peça", opcoes)

        if filtro == "Todas as peças":
            movs = listar_movimentacoes()
        else:
            idx = opcoes.index(filtro) - 1
            movs = listar_movimentacoes(produto_id=produtos_lista[idx][0])

        if movs:
            # Transforma em DataFrame (tabela bonita)
            df = pd.DataFrame(movs, columns=["ID", "Produto ID", "Tipo", "Qtd", "Data/Hora", "Nome"])
            df = df[["Nome", "Tipo", "Qtd", "Data/Hora"]]  # Reordena colunas
            df["Tipo"] = df["Tipo"].apply(lambda x: "🟢 Entrada" if x == "entrada" else "🔴 Saída")

            st.dataframe(df, use_container_width=True, hide_index=True)

            # Resumo rápido
            entradas = df[df["Tipo"] == "🟢 Entrada"]["Qtd"].sum()
            saidas = df[df["Tipo"] == "🔴 Saída"]["Qtd"].sum()

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Entradas", f"{entradas} unid.")
            with col2:
                st.metric("Saídas", f"{saidas} unid.")
        else:
            st.info("Nenhuma movimentação registrada.")
    else:
        st.info("Cadastre peças primeiro.")
