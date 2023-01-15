import streamlit as st
import pandas as pd
import numpy as np
from pydeck.types import String
import pydeck as pdk
from os import path,listdir
import plotly as py
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# Paleta de colores
#=========================================
colorlist=[(0.00, "red"),   (0.33, "red"),(0.33, "yellow"), (0.66, "yellow"), (0.66, "green"),  (1.00, "green")]

st.markdown( #font-weight: 400;
        """
        <style>
          @import url('https://fonts.googleapis.com/css?family=Titillium Web Bold');
          html, body, [class*="css"]  {
          font-family: 'Titillium Web';
          font-size: 28px;
          }
       </style>

       """,
       unsafe_allow_html=True,
       )

new_title = '<p style="font-family:Titillium Web; color:Green; font-size: 38px;">Mapas de Rangos</p>'
st.markdown(new_title, unsafe_allow_html=True)


with open("path.txt",'r',encoding = 'utf-8') as f:
   Path = f.read()
Path = Path.strip()+'/'

cosechas = listdir(Path)

opciones = []
for n in cosechas:
    p = n.split('_')
    cad = ''
    for i,c in enumerate(p):
        cad += c
        if i<len(p)-1:
            cad += ' - '

    opciones.append(cad)

cosecha = st.selectbox(
     "Cuál cosecha desea revisar?",opciones)

file = Path+cosechas[opciones.index(cosecha)]+'/'

rinde = file+'rinde.csv'
resumen = file+'resumen.csv'

st.sidebar.success(f"Procesando: {cosecha}")

# Leer dataframe

if (path.exists(rinde))&(path.exists(resumen)):
    df_rinde = pd.read_csv(rinde)
    df_resumen = pd.read_csv(resumen)
    variables = df_resumen['Variable'].values
    Var = variables.copy()
    var = st.selectbox("Qué varaible desea revisar?",variables)

    df_row = df_resumen[df_resumen['Variable'] == var].copy()
    df_row.reset_index(drop = True,inplace = True)

    etiqueta = df_row.loc[0,'Rangos'].split(';')
    posi = [int(x) for x in df_row.loc[0,'pos'].split(',')]
    etiquetas = [etiqueta[x] for x in posi]

   
    fig = px.scatter(df_rinde, x='x', y='y', color=df_row.loc[0,'Var_capa']+'P',color_continuous_scale = colorlist)
    fig.update_layout(legend=dict(orientation="h"), title_font_color='Green',title_font_family='Titillium Web',width=900,height=600)
    st.write(fig)
    colores = ['red','yellow','green']
    Color = []
    for c in posi:
        Color.append(colores[c])
    fig = go.Figure(data=[go.Table(header=dict(values=['Rango','color']),
        cells=dict(values=[etiquetas,posi],
        fill=dict(color=[['rgb(245,245,245)'],Color] )))])
    fig.update_layout(title_text="Rangos evaluados",title_font_size=28,title_font_color='Green',title_font_family='Titillium Web',width=900,height=600)
    st.write(fig)
else: 
    st.error('Error... file rinde/resumen not found...', icon="🚨")
