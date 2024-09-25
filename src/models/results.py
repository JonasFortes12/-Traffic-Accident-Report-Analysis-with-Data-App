import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import io



def polynomial_regression_victims(datatran, degree=12):
    """
    Função que realiza a regressão polinomial e plota a relação entre número de veículos e a média de vítimas totais.

    Parâmetros:
    - datatran (pd.DataFrame): DataFrame contendo os dados de acidentes de trânsito.
    - degree (int): Grau da regressão polinomial. Padrão é 12.

    Retorna:
    - model: O modelo de regressão linear treinado.
    - poly: O transformador de características polinomiais utilizado.
    - fig: A figura plotada da regressão polinomial.
    """
    # Fazendo uma cópia do dataframe
    datatran_copy = datatran.copy()

    # Criar a variável 'vitimas_totais' utilizando .loc
    datatran_copy.loc[:, 'vitimas_totais'] = (
        datatran_copy.loc[:, 'feridos_leves'] +
        datatran_copy.loc[:, 'feridos_graves'] +
        datatran_copy.loc[:, 'mortos']
    )

    # Agrupando dados por 'veiculos' e calculando a média de 'vitimas_totais'
    grouped_data = datatran_copy.groupby('veiculos')['vitimas_totais'].mean().reset_index()

    # Redefinindo X e y para os dados agrupados como DataFrame
    X_grouped = grouped_data[['veiculos']]  # número de veículos
    y_grouped = grouped_data['vitimas_totais']  # média de vítimas totais

    # Criando características polinomiais de grau definido
    poly = PolynomialFeatures(degree=degree)
    X_poly_grouped = poly.fit_transform(X_grouped)

    # Criando o modelo de Regressão Linear
    model = LinearRegression()

    # Treinando o modelo com os dados transformados
    try:
        model.fit(X_poly_grouped, y_grouped)
    except Exception as e:
        st.error(f"Erro durante o treinamento do modelo: {e}")
        return None, None, None

    # Prevendo valores para os dados agrupados
    y_pred = model.predict(X_poly_grouped)

    # Calculando erros
    mse = mean_squared_error(y_grouped, y_pred)
    mae = mean_absolute_error(y_grouped, y_pred)

    st.info(f"Erro Quadrático Médio (MSE): {mse:.4f}")
    st.info(f"Erro Absoluto Médio (MAE): {mae:.4f}")

    # Prevendo valores para um range contínuo de "veiculos" para suavizar o gráfico
    X_range = np.linspace(X_grouped['veiculos'].min(), X_grouped['veiculos'].max(), 100).reshape(-1, 1)
    X_range_poly = poly.transform(X_range)
    y_range_pred = model.predict(X_range_poly)

    # Criando a figura
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(X_grouped, y_grouped, color='blue', label='Dados Agrupados', alpha=0.5)
    ax.plot(X_range, y_range_pred, color='red', label='Curva de Regressão Polinomial')
    ax.set_title(f'Regressão Polinomial (Grau {degree}): Número de Veículos vs. Média de Vítimas Totais')
    ax.set_xlabel('Número de Veículos')
    ax.set_ylabel('Média de Vítimas Totais')
    ax.legend()
    ax.grid(True)

    # Usando BytesIO para capturar a figura
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)  # Fecha a figura para não sobrecarregar a memória
    buf.seek(0)
    
    return model, poly, buf  # Retornando o modelo, o polinômio e o buffer da figura

