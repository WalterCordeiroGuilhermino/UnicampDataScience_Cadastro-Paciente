"""
Cadastro de Pacientes — versão Streamlit (deploy no Streamlit Community Cloud)
Atividade Prática Aula 1 — Interfaces Web/Mobile para Coleta de Dados

Executar localmente:  streamlit run app.py
"""
import os
from datetime import datetime

import pandas as pd
import streamlit as st

ARQUIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]

st.set_page_config(page_title="Cadastro de Pacientes", page_icon="🏥", layout="centered")
st.title("🏥 Cadastro de Pacientes")
st.caption("Recepção do consultório")

# Acumula os cadastros da sessão
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)

with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox("Convênio", CONVENIOS)
    prioridade = st.slider("Prioridade do atendimento (5 = urgente)", 1, 5, 1)
    motivo = st.text_area("Motivo da consulta / observações")
    enviado = st.form_submit_button("Cadastrar", type="primary", width="stretch")

if enviado:
    if not nome.strip():
        st.warning("Informe o nome do paciente.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo.strip(),
        }
        novo = pd.DataFrame([nova_linha], columns=COLUNAS)

        # 1) Sessão
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, novo], ignore_index=True
        )
        # 2) Mesma lógica de gravação da versão Gradio (arquivo efêmero na nuvem)
        novo.to_csv(ARQUIVO_CSV, mode="a", header=not os.path.exists(ARQUIVO_CSV), index=False)

        st.success(f"Paciente {nova_linha['nome']} cadastrado!")

st.subheader("Últimos pacientes cadastrados")
st.dataframe(st.session_state.pacientes.tail(5), width="stretch", hide_index=True)
st.caption(f"Total cadastrado nesta sessão: {len(st.session_state.pacientes)}")

# O disco do Streamlit Cloud é efêmero → exportar via download
csv = st.session_state.pacientes.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Baixar CSV", csv, "pacientes.csv", "text/csv",
                   width="stretch")
