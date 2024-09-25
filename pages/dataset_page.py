import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.markdown("# Resumo do Dataset 🗂️")
st.sidebar.markdown("#  Resumo do Dataset 🗂️")

DATA_PATH = os.path.join(os.getcwd(), os.path.join('src', 'data', 'datatran2024.csv'))

df = pd.read_csv(DATA_PATH, encoding='latin1', sep=';')
lowercase = lambda x: str(x).lower()
df.rename(lowercase, axis='columns', inplace=True)

# Nome e Descrição do Dataset
st.header("Informações sobre o Dataset")
st.write(f"**Nome do dataset:** {'Traffic Accident Report Analysis'}")

st.subheader("Período de tempo do Dataset")
st.write("01 de Janeiro de 2024 - 31 de Agosto de 2024")

# Tamanho do Dataset
st.subheader("Tamanho do Dataset")
st.write(f"Número de registros (linhas): {df.shape[0]}")
st.write(f"Número de atributos (colunas): {df.shape[1]}")

# Exibindo os Atributos
st.subheader("Amostra dos Dados")
st.write("Primeiras 5 linhas do dataset:")
st.dataframe(df.head())
st.write("Últimas 5 linhas do dataset:")
st.dataframe(df.tail())

# Estatísticas descritivas
st.subheader('Estatísticas Descritivas')
st.write(df.describe())

# Gráfico de barras: Número de acidentes por dia da semana
st.subheader('Número de Acidentes por Dia da Semana')
accidents_by_day = df['dia_semana'].value_counts().sort_index()
st.bar_chart(accidents_by_day)

# Tipos de Dados
st.subheader("Tipos de Dados")
st.write(df.dtypes)

# Exibindo todos os municípios sem repetição
st.subheader("Lista de municípios")
municipios_unicos = df['municipio'].unique()
st.write(municipios_unicos)

# Exibindo todos os municípios sem repetição
st.subheader("Lista de estados")
municipios_unicos = df['uf'].unique()
st.write(municipios_unicos)