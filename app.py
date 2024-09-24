import pandas as pd
import streamlit as st
import plotly.express as px


def carregar_dados_excel(arquivo):
    if arquivo is not None:
        return pd.read_excel(arquivo)
    else:
        return None

#formatar as datas no formato DD/MM/AAAA
def formatar_datas(df, coluna_data):
    df[coluna_data] = pd.to_datetime(df[coluna_data], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
    return df


meses_portugues = {
    'January': 'Janeiro',
    'February': 'Fevereiro',
    'March': 'Março',
    'April': 'Abril',
    'May': 'Maio',
    'June': 'Junho',
    'July': 'Julho',
    'August': 'Agosto',
    'September': 'Setembro',
    'October': 'Outubro',
    'November': 'Novembro',
    'December': 'Dezembro'
}

#"wide" para ocupar a tela toda
st.set_page_config(layout="wide")

st.title('Doações da ONG Arca de Noé')

st.subheader('Carregar Arquivos de Dados em EXCEL, no formato .xlsx')

#Arquivo de Adoções
arquivo_adocoes = st.file_uploader("Upload Arquivo de Adoções", type=["xlsx"])
df_adocoes = carregar_dados_excel(arquivo_adocoes)

#Arquivo de Resgates
arquivo_resgates = st.file_uploader("Upload Arquivo de Resgates", type=["xlsx"])
df_resgates = carregar_dados_excel(arquivo_resgates)

#Arquivo de Doações
arquivo_doacoes = st.file_uploader("Upload Arquivo de Doações", type=["xlsx"])
df_doacoes = carregar_dados_excel(arquivo_doacoes)

# Formatação das datas para exibir no formato DD/MM/AAAA
if df_adocoes is not None:
    df_adocoes = formatar_datas(df_adocoes, 'Data de Adoção')

if df_resgates is not None:
    df_resgates = formatar_datas(df_resgates, 'Data de Resgate')

if df_doacoes is not None:
    df_doacoes = formatar_datas(df_doacoes, 'Data de Doação')

st.subheader('Tabelas e Gráficos')

#ajuste das colunas para ocupar mais espaço na tela
col1, col2, col3 = st.columns([1, 1, 1])

#tabela e gráfico de Adoções na primeira coluna
with col1:
    if df_adocoes is not None:
        st.subheader('Tabela de Adoções')
        st.dataframe(df_adocoes, height=350) #tabela de dados

        #gráfico de Adoções por Mês
        df_adocoes['Data de Adoção'] = pd.to_datetime(df_adocoes['Data de Adoção'], format='%d/%m/%Y')
        df_adocoes['Mês'] = df_adocoes['Data de Adoção'].dt.month_name()
        df_adocoes['Mês'] = df_adocoes['Mês'].map(meses_portugues)  # Traduzir os meses para português
        grafico_adocoes = df_adocoes['Mês'].value_counts().reset_index()
        grafico_adocoes.columns = ['Mês', 'Número de Adoções']
        st.subheader('Adoções por Mês')

        #ajustar o eixo Y para mostrar apenas números inteiros
        fig_adocoes = px.bar(grafico_adocoes, x='Mês', y='Número de Adoções', title='Número de Adoções por Mês')
        fig_adocoes.update_layout(
            yaxis=dict(
                tickmode='linear',
                dtick=1  # Define que as marcas no eixo como inteiros
            )
        )
        st.plotly_chart(fig_adocoes, use_container_width=True)  # Expande o gráfico

#tabela e gráfico de Resgates na segunda coluna
with col2:
    if df_resgates is not None:
        st.subheader('Tabela de Resgates')
        st.dataframe(df_resgates, height=350)  #tabela de dados

        #gráfico de Resgates por Mês
        df_resgates['Data de Resgate'] = pd.to_datetime(df_resgates['Data de Resgate'], format='%d/%m/%Y')
        df_resgates['Mês'] = df_resgates['Data de Resgate'].dt.month_name()
        df_resgates['Mês'] = df_resgates['Mês'].map(meses_portugues)  # Traduzir os meses para português
        
        ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        
        grafico_resgates = df_resgates['Mês'].value_counts().reset_index()
        grafico_resgates.columns = ['Mês', 'Número de Resgates']
        
        st.subheader('Resgates por Mês')
        fig_resgates = px.bar(grafico_resgates, x='Mês', y='Número de Resgates', title='Número de Resgates por Mês', 
                              category_orders={'Mês': ordem_meses})  # Definir a ordem dos meses
        st.plotly_chart(fig_resgates, use_container_width=True)  # Expande o gráfico

#tabela e gráfico de Doações na terceira coluna
with col3:
    if df_doacoes is not None:
        st.subheader('Tabela de Doações')
        st.dataframe(df_doacoes, height=350)  #tabela de dados

        #seleção de mês para o gráfico
        df_doacoes['Data de Doação'] = pd.to_datetime(df_doacoes['Data de Doação'], format='%d/%m/%Y')
        df_doacoes['Mês'] = df_doacoes['Data de Doação'].dt.month_name()
        df_doacoes['Mês'] = df_doacoes['Mês'].map(meses_portugues)  # Traduzir os meses para português
        meses_disponiveis = df_doacoes['Mês'].unique()

        #selectbox para escolher o mês
        mes_selecionado = st.selectbox('Selecione o mês para o gráfico de doações:', options=meses_disponiveis)

        #siltrar os dados de doações com base no mês selecionado
        df_doacoes_filtrado = df_doacoes[df_doacoes['Mês'] == mes_selecionado]

        #gráfico de Doações por Tipo para o mês selecionado
        grafico_doacoes = df_doacoes_filtrado['Tipo de Doação'].value_counts().reset_index()
        grafico_doacoes.columns = ['Tipo de Doação', 'Quantidade']
        st.subheader(f'Distribuição de Doações por Tipo para {mes_selecionado}')
        fig_doacoes = px.pie(grafico_doacoes, names='Tipo de Doação', values='Quantidade', title=f'Distribuição de Doações por Tipo para {mes_selecionado}')
        st.plotly_chart(fig_doacoes, use_container_width=True)
