import streamlit as st
import os

with open(os.path.join(os.getcwd(), 'README.md'), 'r', encoding='utf-8') as file:
    markdown_text = file.read()


st.markdown(markdown_text, unsafe_allow_html=True)

st.title("Acesse o App")
st.write("Escaneie o QR code abaixo para acessar o app no seu dispositivo:")

# Caminho da imagem do QR code já salva (coloque o caminho correto aqui)
qr_image_path = os.path.join(os.getcwd(), 'assets\QRCode.svg')

# Exibir o QR code na página
st.image(qr_image_path, caption="Ou acesse: https://traffic-accident-report-analysis.streamlit.app/",  width=300)
