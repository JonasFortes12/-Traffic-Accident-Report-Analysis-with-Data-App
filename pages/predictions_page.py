import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from src.data.statistics import get_dataset
from src.models.results import polynomial_regression_victims
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import plotly.graph_objects as go


st.markdown("# Resultados dos Modelos 🎯")
st.sidebar.markdown("# Resultados dos Modelos 🎯")

# Criação das abas
tab1, tab2 = st.tabs(["Regressão Veículo x Vítimas", "Classificação de Acidentes"])

# Conteúdo da aba 1
with tab1:
    st.subheader("Resultados do Modelo: Regressão Veículo x Vítimas")
    
    dataset = get_dataset()
    degree = st.number_input('Selecione o grau da regressão polinomial:', min_value=1, max_value=20, value=12)
    # Chamando a função
    model, poly, fig_buffer = polynomial_regression_victims(dataset, degree)
    
    if fig_buffer:
        st.image(fig_buffer, caption='Regressão Polinomial', use_column_width=True)
    
    # Campo para entrada de quantidade de veículos
    veiculos = st.number_input('Digite a quantidade de veículos:', min_value=0)

    # Previsão
    if st.button('Prever vítimas'):
        if model and poly:
            X_new = poly.transform(np.array([[veiculos]]))
            prediction = model.predict(X_new)
            st.success(f'Previsão da média de vítimas: {prediction[0]:.2f}')


# Conteúdo da aba 2
with tab2:
    st.subheader("Previsão de Classificação de Acidentes")
 
    def fazer_predicao(model, nova_entrada_valores, datatran_copy, label_encoders, label_encoder):
        # Transformando a nova entrada
        nova_entrada = pd.DataFrame(nova_entrada_valores)

        # Aplicando Label Encoding na nova entrada
        for coluna in label_encoders.keys():
            nova_entrada[coluna] = label_encoders[coluna].transform(nova_entrada[coluna])

        # Fazendo a predição para a nova entrada
        nova_predicao = model.predict(nova_entrada)
        nova_predicao_categ = label_encoder.inverse_transform(nova_predicao)

        # Definindo as cores para cada classe
        color_map = {
            label_encoder.classes_[0]: 'red', 
            label_encoder.classes_[1]: 'orange', 
            label_encoder.classes_[2]: 'green'
        }
        
        nova_entrada['classificacao_predita'] = nova_predicao_categ[0]
        nova_entrada['color'] = 'blue'  # A cor azul é atribuída à nova entrada

        # Convertendo a nova entrada de volta para categórica
        for coluna in label_encoders.keys():
            nova_entrada[coluna] = label_encoders[coluna].inverse_transform(nova_entrada[coluna])

        # Fazendo predições para todas as linhas do DataFrame original (datatran_copy)
        X_todas = datatran_copy[['dia_semana', 'fase_dia', 'uf']]
        y_pred_todas = model.predict(X_todas)

        # Adicionando as predições ao DataFrame original
        datatran_copy['classificacao_predita'] = label_encoder.inverse_transform(y_pred_todas)

        # Convertendo as features de volta para categórico
        for coluna in label_encoders.keys():
            datatran_copy[coluna] = label_encoders[coluna].inverse_transform(datatran_copy[coluna])

        # Adicionando as cores com base nas predições
        datatran_copy['color'] = datatran_copy['classificacao_predita'].map(color_map)

        # Adicionando a nova entrada ao DataFrame original
        datatran_copy = pd.concat([datatran_copy, nova_entrada], ignore_index=True)

        # Criando um gráfico 3D interativo com todas as predições
        fig = px.scatter_3d(
            datatran_copy,
            x='dia_semana',
            y='fase_dia',
            z='uf',
            color='classificacao_predita',
            color_discrete_map=color_map,
            labels={'classificacao_predita': 'Classificação do Acidente'},
            title='Classificação de Acidentes em 3D'
        )

        # Adicionando um ponto azul para a nova entrada como um traço separado
        fig.add_trace(go.Scatter3d(
            x=nova_entrada['dia_semana'],
            y=nova_entrada['fase_dia'],
            z=nova_entrada['uf'],
            mode='markers+text',
            marker=dict(size=10, color='blue'),
            text=nova_entrada['classificacao_predita'],
            textposition='top center',
            name='Valor predito'
        ))

        # Exibindo a classificação predita no console
        st.info(f'Classificação predita para a nova entrada: {nova_predicao_categ[0]}')

        # Exibindo o gráfico
        st.plotly_chart(fig)

        return datatran_copy  # Retornando o DataFrame atualizado
        
    # Entradas do usuário
    dia_semana = st.selectbox("Selecione o dia da semana", ['segunda feira', 'terça feira', 'quarta feira', 'quinta feira', 'sexta feira', 'sábado', 'domingo'])
    fase_dia = st.selectbox("Selecione a fase do dia", ['Amanhecer', 'Anoitecer', 'Pleno dia', 'Plena Noite'])
    
    uf = st.selectbox("Selecione o estado (UF)", ['ES', 'PI', 'BA', 'SE', 'MT', 'MG', 'SP', 'PR', 'MS', 'RS', 'PA', 'GO', 'RJ', 'PB',
                        'MA', 'SC', 'PE', 'TO', 'AL', 'RO', 'CE', 'RN', 'DF', 'AM', 'AC', 'RR', 'AP'])

    # Estrutura de dados da nova entrada
    nova_entrada_valores = {
        'dia_semana': [dia_semana],
        'fase_dia': [fase_dia],
        'uf': [uf]
    }

    # Carregando os dados e treinando o modelo (exemplo)
    datatran_copy = get_dataset()  # Função para carregar os dados
    datatran_copy['dia_semana'] = datatran_copy['dia_semana'].replace({'segunda-feira': 'segunda feira', 'terça-feira': 'terça feira', 'quarta-feira': 'quarta feira',
                                                         'quinta-feira': 'quinta feira', 'sexta-feira': 'sexta feira'})
    
    
    label_encoders = {}
    for column in ['dia_semana', 'fase_dia', 'uf']:
        le = LabelEncoder()
        datatran_copy[column] = le.fit_transform(datatran_copy[column])
        label_encoders[column] = le

    # Convertendo 'classificacao_acidente' usando Label Encoding
    label_encoder = LabelEncoder()
    datatran_copy['classificacao_acidente'] = label_encoder.fit_transform(datatran_copy['classificacao_acidente'])

    # Definindo as features (X) e o alvo (y)
    X = datatran_copy[['dia_semana', 'fase_dia', 'uf']]
    y = datatran_copy['classificacao_acidente']

    # Dividindo os dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinando o modelo RandomForest
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    
    # Botão para fazer a predição
    if st.button("Fazer Predição"):
        # Realizando a predição e atualizando o DataFrame
        datatran_copy = fazer_predicao(model, nova_entrada_valores, datatran_copy, label_encoders, label_encoder)