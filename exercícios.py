import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Automatizador de Painéis",
    page_icon="bar_chart:",
    layout="wide"
)

# Função para carregar o arquivo Excel
def load_excel(file):
    # Ler o arquivo Excel (.xlsx) em um DataFrame
    df = pd.read_excel(file, engine='openpyxl', skiprows=4)
    return df

# Interface do usuário
st.title("Visualizador de Planilhas Excel")

# Upload do arquivo
with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.sidebar.file_uploader("Escolha um arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Carregar o DataFrame
    df = load_excel(uploaded_file)

    # Mostrar o DataFrame de forma visual
    st.write("Conteúdo do DataFrame:")
    st.dataframe(df)

    # Exibir informações adicionais sobre o DataFrame
    st.write("Informações do DataFrame:")
    st.write(df.info())

    # Separar as seções por linhas
    st.write("---")  # Linha de separação

    # Contagem de Status e Processos a Distribuir
    st.markdown("""
        <h2 style="font-size: 28px; text-decoration: underline; text-align: center;">
            Contagem de Status e Processos a Distribuir
        </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <h3 style="text-decoration: underline; text-align: center;">
                Contagem de Processos por Responsável e Status:
            </h3>
        """, unsafe_allow_html=True)

        status_counts_by_responsible = df[df['Adimplência (última emissão)'].isin(['Solicitado', 'Inadimplente'])]
        status_counts_by_responsible = status_counts_by_responsible.groupby(
            ['RESPONSÁVEL', 'Adimplência (última emissão)']).size().unstack(fill_value=0).reset_index()

        # Ajuste para garantir a exibição sem coluna extra e centralizar
        styled_status_counts = status_counts_by_responsible.style.set_properties(
            **{'text-align': 'center', 'width': '150px'}
        ).set_table_styles(
            [{'selector': 'thead th', 'props': 'text-align: center;'}]
        )

        st.write(styled_status_counts, use_container_width=True)

    with col2:
        st.markdown("""
            <h3 style="text-decoration: underline; text-align: center;">
                Processos que Devem Ser Distribuídos:
            </h3>
        """, unsafe_allow_html=True)

        # Filtrar dados
        filtered_df = df[
            (df['Ano-Sanfom'] == 2024) &
            (df['INSTRUÇÃO PROCESSUAL CONCLUÍDA?'] == 'SIM') &
            (df['ANALISTA'].isna())
            ]

        # Selecionar apenas as colunas do título do projeto, o número do processo e SANFOM
        filtered_df = filtered_df[['TÍTULO DO PROJETO', 'Nº PROCESSO', 'SANFOM']]

        # Contar o número total de processos
        num_processes = len(filtered_df)

        # Exibir o DataFrame e o número total de processos
        st.write(filtered_df, use_container_width=True)
        st.markdown(f"""
        <div style="font-size: 24px; font-weight: bold; text-align: center;">
            Processos a Distribuir<br>
            <span style="font-size: 36px;">{num_processes}</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")  # Linha de separação

    # Inadimplentes e Adimplências Vencidas
    st.markdown("""
        <h2 style="font-size: 28px; text-decoration: underline; text-align: center;">
            Inadimplentes e Adimplências Vencidas
        </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <h3 style="text-decoration: underline; text-align: center;">
                Quadro de Inadimplentes:
            </h3>
        """, unsafe_allow_html=True)

        # Filtrar processos inadimplentes
        inadimplentes_df = df[df['Adimplência (última emissão)'] == 'Inadimplente'][['Nº PROCESSO', 'TÍTULO DO PROJETO', 'SANFOM']]

        # Exibir o DataFrame com os processos inadimplentes
        st.write(inadimplentes_df, use_container_width=True)

    with col2:
        st.markdown("""
            <h3 style="text-decoration: underline; text-align: center;">
                Adimplências Vencidas:
            </h3>
        """, unsafe_allow_html=True)

        # Converter a coluna 'Vigência Adimplência' para datetime e filtrar
        df['Vigência Adimplência'] = pd.to_datetime(df['Vigência Adimplência'], errors='coerce')
        today = datetime.today()
        vencidas_df = df[(df['Vigência Adimplência'].notna()) & (df['Vigência Adimplência'] < today)]
        vencidas_df = vencidas_df[['Nº PROCESSO', 'TÍTULO DO PROJETO', 'SANFOM']]

        # Exibir o DataFrame com as adimplências vencidas
        st.write(vencidas_df, use_container_width=True)

    st.write("---")  # Linha de separação

    # Filtrar Processos por Analista
    st.markdown("""
        <h2 style="font-size: 28px; text-decoration: underline; text-align: center;">
            Filtrar Processos por Analista:
        </h2>
    """, unsafe_allow_html=True)

    # Obter a lista de analistas únicos
    analistas = df['ANALISTA'].dropna().unique()
    analista_selected = st.selectbox("Escolha um Analista", ["Todos"] + list(analistas))

    if analista_selected != "Todos":
        filtered_analista_df = df[df['ANALISTA'] == analista_selected]
    else:
        filtered_analista_df = df

    # Selecionar as colunas a serem exibidas
    filtered_analista_df = filtered_analista_df[['Nº PROCESSO', 'TÍTULO DO PROJETO', 'SANFOM']]

    # Exibir o DataFrame filtrado
    st.write(filtered_analista_df, use_container_width=True)
