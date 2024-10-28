#LINK PARA OS DADOS NO GOVERNO https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis
#LINK PARA OS emoji shortcodes https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.express as px

#CONFIGURAÇÃO DA PAGINA
st.set_page_config(page_title='Analise_Combustivel\Preços Anual 2023', page_icon=':fire:', initial_sidebar_state='auto', layout='wide')
st.sidebar.title(':oil_drum:_Painel de Controle_')

# TÍTULO E IMAGEM DE CAPA
imagems = 'D:\Área de Trabalho\Meus Projetos Python\streamlit\Analise_Combustivel - Copia\istockphoto-1136053255-2048x2048.jpg'
st.title(':fire: _Análise Exclusiva: Preços de Combustíveis em_ :green[2023]')
st.image(imagems, caption='Preços de Combustíveis')

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

#st.title('_Analise de Combustíve de_ :green[2023]')
st.subheader('**Uma visão detalhada sobre as variações de preços e consumo de combustíveis ao longo do ano de 2023**')
st.header('', divider='rainbow')

# CRIANDO COLUNAS
col1, col2 = st.columns(2)
col3 = st.columns(1)[0]
col4, col5 = st.columns(2)
col6, col7 = st.columns(2)

# SELEÇÃO DO COMBUSTÍVEL
tipo_combus = dados['Produto'].unique()
selecao_combust = st.sidebar.selectbox('Selecione o Combustível', tipo_combus)

# MAIOR E MENOR PREÇO
menor_preco = dados.loc[dados['Valor de Venda'].idxmin()]
maior_preco = dados.loc[dados['Valor de Venda'].idxmax()]

# MAIOR E MENOR PREÇO NA COLUNA COMO DESCRIÇÃO
with col1:
    st.write('Maior Preço Registrado:', maior_preco['Data da Coleta'],'R$:',maior_preco['Valor de Venda'],'-', maior_preco['Municipio'],'-',
              maior_preco['Estado - Sigla'], '-', maior_preco['Produto'])
    
with col2:
    st.write('Menor Preço Registrado:', menor_preco['Data da Coleta'],'R$:',menor_preco['Valor de Venda'], '-', menor_preco['Municipio'],'-',
              menor_preco['Estado - Sigla'], '-', menor_preco['Produto'])

# APRESENTAÇÃO DO GRÁFICO
with col3:
    st.write('Grafico')
    dados['MES'] = dados['Data da Coleta'].apply(lambda x: str(x.year) + '-' + str(x.month))
    filtro = dados[dados['Produto'] == selecao_combust].groupby('Estado - Sigla')['Valor de Venda'].mean().reset_index()

    # Criar o gráfico
    fig = px.bar(filtro, x='Estado - Sigla', y='Valor de Venda', title="Gráfico de Preços por Estado")
    st.plotly_chart(fig)

# MÉDIA DE PREÇO POR MUNICÍPIO E TIPO DE COMBUSTÍVEL    
with col4:
    st.subheader('Média de Preço por Municipio e Tipo de Combustível')

    preco_combust_selecionado = dados[dados['Produto'] == selecao_combust].groupby(['Municipio','Estado - Sigla'])['Valor de Venda'].mean().reset_index()
    preco_combust_selecionado = preco_combust_selecionado.sort_values(by='Valor de Venda', ascending=False)
    st.write(preco_combust_selecionado)
    print(preco_combust_selecionado.columns)

# MÉDIA DE PREÇO POR ESTADO E TIPO DE COMBUSTÍVEL
with col5:
    st.subheader('Média de Preço por estado e tido de combustível')
    preco_combust_estado = dados[dados['Produto'] == selecao_combust].groupby(['Estado - Sigla','Bandeira'])['Valor de Venda'].mean()
    preco_combust_estado = preco_combust_estado.sort_values(ascending=False)
    st.write(preco_combust_estado)
    print(preco_combust_estado)

# CONCLUSÕES
with col6:

    st.header('Conclusões')
    st.write('A análise dos preços de combustíveis em 2023 revelou que:')
    st.write('* O maior preço registrado foi de R$ {:.2f} em {}'.format(maior_preco['Valor de Venda'], maior_preco['Municipio']))
    st.write('* O menor preço registrado foi de R$ {:.2f} em {}'.format(menor_preco['Valor de Venda'], menor_preco['Municipio']))
    st.write('* A média de preço por estado é:')
    st.write(preco_combust_estado)

# RECOMENDAÇÕES
with col7:
        
    st.header('Recomendações')
    st.write('Com base na análise, recomendamos:')
    st.write('* Monitorar os preços de combustíveis em diferentes estados e municípios')
    st.write('* Avaliar a relação entre os preços de combustíveis e a economia local')
    st.write('* Desenvolver estratégias para reduzir os custos de combustíveis')

#RODAPÉ
footer="""<style>
a:link , a:visited{
color: green;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: right;
}
</style>
<div class="footer">
Developed with 📊 by <a style='display: block; text-align: right;' href="https://www.linkedin.com/in/lucianoherval/" target="_blank">Luciano Herval S. L. Filho</a>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

