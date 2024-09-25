import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from src.data.statistics import get_dataset
from src.models.results import polynomial_regression_victims

st.markdown("# Models Results 🎯")
st.sidebar.markdown("# Models Results 🎯")

# Criação das abas
tab1, tab2, tab3 = st.tabs(["Regressão Veículo x Vítimas", "Modelo 2", "Modelo 3"])

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
            st.write(f'Previsão de vítimas para {veiculos} veículos: {prediction[0]:.2f}')

# Conteúdo da aba 2
with tab2:
    st.subheader("Resultados do Modelo 2")
    st.write("Aqui você pode incluir informações sobre o segundo modelo.")
    # Exemplo de gráfico
    # st.bar_chart(data2)

# Conteúdo da aba 3
with tab3:
    st.subheader("Resultados do Modelo 3")
    st.write("Aqui você pode incluir informações sobre o terceiro modelo.")
    # Exemplo de gráfico
    # st.scatter_chart(data3)

# Lembre-se de substituir os comentários de exemplo por seus próprios dados e visualizações.