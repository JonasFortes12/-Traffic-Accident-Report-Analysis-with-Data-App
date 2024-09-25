import streamlit as st

st.markdown("# Models Results 🎯")
st.sidebar.markdown("# Models Results 🎯")

# Criação das abas
tab1, tab2, tab3 = st.tabs(["Modelo 1", "Modelo 2", "Modelo 3"])

# Conteúdo da aba 1
with tab1:
    st.subheader("Resultados do Modelo 1")
    st.write("Aqui você pode incluir informações sobre o primeiro modelo, como métricas de desempenho, gráficos e visualizações.")
    # Exemplo de gráfico
    # st.line_chart(data1)

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