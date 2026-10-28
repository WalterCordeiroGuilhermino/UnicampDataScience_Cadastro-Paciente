# Cadastro de Pacientes — Gradio x Streamlit

Atividade Prática Aula 1 — Interfaces Web/Mobile para Coleta de Dados.

Sistema de cadastro de pacientes para a recepção de um consultório, implementado duas vezes:

| Pasta | Biblioteca | Onde roda | Persistência |
|---|---|---|---|
| `gradio_app/` | Gradio (`gr.Blocks`) | Local | `pacientes.csv` no disco |
| `streamlit_app/` | Streamlit (`st.form`) | Streamlit Community Cloud | `st.session_state` + botão de download do CSV |

**App publicado:** <COLE AQUI O LINK .streamlit.app>

## Campos
Nome, Idade, Convênio (Particular, Unimed, Bradesco Saúde, SulAmérica, Outro), Prioridade (1–5, 5 = urgente), Motivo/observações. Cada envio grava uma linha com data/hora.

## Como rodar

```bash
pip install -r streamlit_app/requirements.txt

# Gradio
python gradio_app/app.py            # http://127.0.0.1:7860

# Streamlit
streamlit run streamlit_app/app.py  # http://localhost:8501
```

## Comparação

| | Gradio | Streamlit |
|---|---|---|
| Modelo | Eventos (botão → função) | Script re-executado a cada interação |
| Formulário | Componentes soltos ligados por `click` | `st.form` agrupa e envia de uma vez |
| Estado | Arquivo CSV / `gr.State` | `st.session_state` |
| Publicação | Link temporário (`share=True`) ou Hugging Face Spaces | Streamlit Community Cloud direto do GitHub |
| Limitação | Link `share` expira em 72h | Disco efêmero → precisa do download do CSV |

`pacientes.csv` é um arquivo de exemplo gerado nos testes.
