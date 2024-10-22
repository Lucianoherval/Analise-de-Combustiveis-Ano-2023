#LINK PARA OS DADOS NO GOVERNO https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis
#LINK PARA OS emoji shortcodes https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
import pandas as pd
import streamlit as st
from datetime import datetime

#CONFIGURAÇÃO DA PAGINA
st.set_page_config(page_title='Analise_Combustivel\Preços Anual 2023', page_icon=':oil_drum:', initial_sidebar_state='auto', layout='wide')
st.sidebar.title(':oil_drum:_Painel de Controle_')

#LEITURA DOS DADOS DE FORMA CORRETA
dados_base1 = pd.read_csv(r'D:\Área de Trabalho\Meus Projetos Python\streamlit\Analise_Combustivel\Preços semestrais - AUTOMOTIVOS_2023.01.csv', sep=';', decimal=',')
dados_base2 = pd.read_csv(r'D:\Área de Trabalho\Meus Projetos Python\streamlit\Analise_Combustivel\Preços semestrais - AUTOMOTIVOS_2023.02.csv', sep=';', decimal=',')
#FUNDINDO OS 2 DADOS BASES
dados_base3 = pd.concat([dados_base1, dados_base2], ignore_index=True)

#SELEÇÃO DE COLUNAS UTEIS
dados = dados_base3[['Data da Coleta','Municipio','Estado - Sigla','Produto','Valor de Venda','Unidade de Medida','Bandeira']]
dados['Data da Coleta'] = pd.to_datetime(dados['Data da Coleta'], format='%d/%m/%Y', dayfirst=True).dt.date

#LIMPEZA DOS DADOS
dados.isna().sum()
dados.fillna(0)

print(dados.info())

st.title('_Analise de Combustíve de_ :green[2023]')
st.subheader('**Uma visão detalhada sobre as variações de preços e consumo de combustíveis ao longo do ano de 2023**')
st.header('', divider='rainbow')

col1, col2 = st.columns(2)
col3 = st.columns(1)[0]
col4, col5 = st.columns(2)


menor_preco = dados.loc[dados['Valor de Venda'].idxmin()]
maior_preco = dados.loc[dados['Valor de Venda'].idxmax()]

with col1:
    st.write('Maior Preço Registrado:', maior_preco['Data da Coleta'],'R$:',maior_preco['Valor de Venda'],'-', maior_preco['Municipio'],'-',
              maior_preco['Estado - Sigla'], '-', maior_preco['Produto'])
    
with col2:
    st.write('Menor Preço Registrado:', menor_preco['Data da Coleta'],'R$:',menor_preco['Valor de Venda'], '-', menor_preco['Municipio'],'-',
              menor_preco['Estado - Sigla'], '-', menor_preco['Produto'])
    
with col3:
    st.write('Grafico')
    
with col4:
    st.subheader('Média de Preço por Municipio e Tipo de Combustível')
    tipo_combus = dados['Produto'].unique()
    selecao_combust = st.sidebar.selectbox('Selecione o Combustível', tipo_combus)
    preco_combust_selecionado = dados[dados['Produto'] == selecao_combust].groupby(['Municipio','Estado - Sigla'])['Valor de Venda'].mean().reset_index()
    preco_combust_selecionado = preco_combust_selecionado.sort_values(by='Valor de Venda', ascending=False)
    st.write(preco_combust_selecionado)
    print(preco_combust_selecionado.columns)

with col5:
    st.subheader('Média de Preço por estado e tido de combustível')
    preco_combust_estado = dados[dados['Produto'] == selecao_combust].groupby(['Estado - Sigla','Bandeira'])['Valor de Venda'].mean()
    preco_combust_estado = preco_combust_estado.sort_values(ascending=False)
    st.write(preco_combust_estado)
    print(preco_combust_estado)

