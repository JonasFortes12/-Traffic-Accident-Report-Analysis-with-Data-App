import streamlit as st
from src.data.statistics import *

st.markdown("# Estatísticas 📊")
st.sidebar.markdown("# Estatísticas 📊")

# Carregar seu dataset
df = get_dataset()

# ------------------------------------------------
st.title('Estatísticas Gerais de Acidentes de Trânsito')

# Chamar a função general_statistics para obter os dados
general_stats = general_statistics(df)

st.metric("Total de Acidentes", general_stats['Total Accidents'])
st.metric("Total de Mortes", general_stats['Total Deaths'])
st.metric("Total de Feridos Leves", general_stats['Total Minor Injuries'])
st.write(f"Período do Dataset: {general_stats['Dataset Time Period']}")
st.metric("Taxa de Fatalidade (%)", general_stats['Fatality Rate (%)'])

# ------------------------------------------------
st.title('Estatísticas de Severidade dos Acidentes')

# Obter estatísticas de severidade de acidentes
severity_df = accident_severity(df)

# Plotando os níveis de severidade usando Streamlit
st.bar_chart(severity_df.set_index('Severity'))

# ------------------------------------------------
st.title("Análise de Acidentes de Trânsito")

# Obter estatísticas
cause_df = main_causes(df)
classification_df = accident_classification(df)
type_df = common_accident_types(df)

# Principais Causas
st.subheader("Principais Causas dos Acidentes")
st.bar_chart(cause_df.set_index('Cause'))

# Classificação dos Acidentes
st.subheader("Classificação dos Acidentes")
st.bar_chart(classification_df.set_index('Classification'))

# Tipos Comuns de Acidentes
st.subheader("Tipos Comuns de Acidentes")
st.bar_chart(type_df.set_index('Accident Type'))

# ------------------------------------------------
st.title("Análise das Condições Ambientais")

# Obter estatísticas das condições ambientais
weather_df = weather_conditions(df)
direction_df = road_direction(df)
type_df = road_type(df)

# Condições Meteorológicas
st.subheader("Condições Meteorológicas")
st.bar_chart(weather_df.set_index('Weather Condition'))

# Direção da Estrada
st.subheader("Direção da Estrada")
st.bar_chart(direction_df.set_index('Road Direction'))

# Tipo de Estrada
st.subheader("Tipo de Estrada")
st.bar_chart(type_df.set_index('Road Type'))

# ------------------------------------------------

mapa = create_heatmap(df)

# Exibindo o mapa no Streamlit
st.subheader("Mapa de Calor de Acidentes de Trânsito")
st_folium(mapa, width=725)