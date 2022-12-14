### Contents of the main file ###
import streamlit as st
from PIL import Image

# Tomar nombre de usuario
#====================================
path = 'Ledezma'

# Guardar en un txt para pasarlo como par谩metro
#======================================================
with open("path.txt",'w',encoding = 'utf-8') as f:
   f.write(path)


im = Image.open("favico.ico")
st.set_page_config(
    page_title="Hello",
    page_icon=im,layout="wide"
)

st.write("# Welcome to AgroSamart! 馃憢")

#st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Somos una empresa dedicada al an谩lisis de los datos de tus procesos productivos. Por medio de la revisi贸n minuciosa del dato podemos encontrar patrones ocultos que nos periten determinar qu茅 elementos/variables  pueden ser objeto de revisi贸n para optimizar y mejorar el proceso productivo, con el prop贸sito de generar mayores ganancias optimizando los recursos, haciendo uso eficiente de estos. Este proceso se lleva a cabo por medio de la utilizaci贸n de tecnolog铆a de Inteligencia Artificial de vanguardia, y que ya ha sido probada y validada en varios procesos de producci贸n agr铆cola.
"""
)

image = Image.open('icono.jpg')

st.image(image, use_column_width = True, caption='by AgroSmart')

image_int = Image.open('integrantes.jpg')

st.image(image_int, use_column_width = True, caption='by AgroSmart')


