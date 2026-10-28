"""
Cadastro de Pacientes — versão Gradio (execução local)
Atividade Prática Aula 1 — Interfaces Web/Mobile para Coleta de Dados

Executar:  python app.py   →  abre em http://127.0.0.1:7860
"""
import os
from datetime import datetime

import gradio as gr
import pandas as pd

# CSV salvo na mesma pasta do app, independente de onde o comando é executado
ARQUIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]


def carregar_ultimos(n: int = 5) -> pd.DataFrame:
    """Retorna os últimos n pacientes do CSV (ou tabela vazia)."""
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV).tail(n)
    return pd.DataFrame(columns=COLUNAS)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    # Validação simples dos campos obrigatórios
    if not nome or not nome.strip():
        return "⚠️ Informe o nome do paciente.", carregar_ultimos()
    if idade is None or idade < 0 or idade > 120:
        return "⚠️ Informe uma idade válida (0 a 120).", carregar_ultimos()
    if not convenio:
        return "⚠️ Selecione o convênio.", carregar_ultimos()

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": (motivo or "").strip(),
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    # Cria o arquivo com cabeçalho na 1ª execução; depois só acrescenta linhas
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    return f"✅ Paciente {linha['nome']} cadastrado com sucesso!", carregar_ultimos()


# Layout em coluna única → funciona bem na tela do celular
with gr.Blocks(title="Cadastro de Pacientes") as demo:
    gr.Markdown("## 🏥 Cadastro de Pacientes\nRecepção do consultório")

    nome = gr.Textbox(label="Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = gr.Number(label="Idade", precision=0, minimum=0, maximum=120)
    convenio = gr.Dropdown(CONVENIOS, label="Convênio", value="Particular")
    prioridade = gr.Slider(1, 5, step=1, value=1,
                           label="Prioridade do atendimento (5 = urgente)")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    botao = gr.Button("Cadastrar", variant="primary")

    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(value=carregar_ultimos(),
                          label="Últimos pacientes cadastrados",
                          interactive=False)

    botao.click(
        cadastrar_paciente,
        [nome, idade, convenio, prioridade, motivo],
        [saida_msg, tabela],
    )

if __name__ == "__main__":
    demo.launch()
