import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Automatizador de Painéis",
    page_icon="bar_chart:",
    layout="wide"
)

# Função para carregar o arquivo Excel
def load_excel(file, file_type):
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
    # Obter o tipo do arquivo
    file_type = uploaded_file.name.split('.')[-1]

    # Carregar o DataFrame
    df = load_excel(uploaded_file, file_type)

    # Mostrar o DataFrame de forma visual
    st.write("Conteúdo do DataFrame:")
    st.dataframe(df)

    # Exibir informações adicionais sobre o DataFrame
    st.write("Informações do DataFrame:")
    st.write(df.info())

    # Separar as seções por linhas
    st.write("---")  # Linha de separação

    # Contagem de Status
    st.markdown("""
        <h2 style="font-size: 28px; text-decoration: underline; text-align: center;">
            Contagens de Status:
        </h2>
    """, unsafe_allow_html=True)

    # Contar apenas 'Solicitado' e 'Inadimplente'
    status_counts = df['Adimplência (última emissão)'].value_counts()
    requested_inadimplente_counts = status_counts[status_counts.index.isin(['Solicitado', 'Inadimplente'])]

    # Mostrar as contagens como métricas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="font-size: 24px; font-weight: bold; text-align: center;">
            Solicitado<br>
            <span style="font-size: 36px;">{requested_inadimplente_counts.get('Solicitado', 0)}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="font-size: 24px; font-weight: bold; text-align: center;">
            Inadimplente<br>
            <span style="font-size: 36px;">{requested_inadimplente_counts.get('Inadimplente', 0)}</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")  # Linha de separação

    # Colunas para exibir dataframes lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <h2 style="font-size: 28px; text-decoration: underline; text-align: center;">
                Contagem de Processos por Responsável e Status:
            </h2>
        """, unsafe_allow_html=True)

        status_counts_by_responsible = df[df['Adimplência (última emissão)'].isin(['Solicitado', 'Inadimplente'])]
        status_counts_by_responsible = status_counts_by_responsible.groupby(
            ['RESPONSÁVEL', 'Adimplência (última emissão)']).size().unstack(fill_value=0).reset_index()

        # Ajuste para garantir a exibição sem coluna extra e centralizar
        styled_status_counts = status_counts_by_responsible.style.set_properties(
            **{'text-align': 'center', 'width': '150px'}
        ).set_table_styles(
            [{'selector': 'thead th', 'props': 'text-align: center;'}]
        ).hide(axis='index')  # Oculta o índice

        st.write(styled_status_counts, use_container_width=True)

    with col2:
        st.markdown("""
            <h2 style="font-size: 28px; text-decoration: underline; text-align: center;">
                Processos que Devem Ser Distribuídos:
            </h2>
        """, unsafe_allow_html=True)

        # Filtrar dados
        filtered_df = df[
            (df['Ano-Sanfom'] == 2024) &
            (df['INSTRUÇÃO PROCESSUAL CONCLUÍDA?'] == 'SIM') &
            (df['ANALISTA'].isna())
            ]

        # Selecionar apenas as colunas do título do projeto e o número do processo
        filtered_df = filtered_df[['TÍTULO DO PROJETO', 'Nº PROCESSO']]

        st.write(filtered_df, use_container_width=True)

        # Contar o número total de processos
        num_processes = len(filtered_df)

        # Exibir o número total de processos com uma tag visual
        st.markdown(f"""
        <div style="font-size: 24px; font-weight: bold; text-align: center;">
            Processos a Distribuir<br>
            <span style="font-size: 36px;">{num_processes}</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")  # Linha de separação
