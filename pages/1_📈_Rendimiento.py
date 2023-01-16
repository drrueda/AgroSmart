### Contents of pages/Colision_Range.py ###
import streamlit as st
import pandas as pd
import numpy as np
from os import path,listdir
import plotly as py
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

fontsize = 16
st.markdown( #font-weight: 400;
        """
        <style>
          @import url('https://fonts.googleapis.com/css?family=Titillium Web Bold');
          html, body, [class*="css"]  {
          font-family: 'Titillium Web Bold';
          font-size: 16px;
          }
       </style>

       """,
       unsafe_allow_html=True,
       )

new_title = '<p style="font-family:Titillium Web Bold; color:Green; font-size: 20px;">Rendimiento</p>'
st.markdown(new_title, unsafe_allow_html=True)

with open("path.txt",'r',encoding = 'utf-8') as f:
   Path = f.read()
Path = Path.strip()+'/'
#st.write(path)

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
     "Cuál cosecha desea revisar?",
     opciones
)

file = Path+cosechas[opciones.index(cosecha)]+'/'

rinde = file+'rinde.csv'
resumen = file+'resumen.csv'

st.sidebar.success(f"Procesando: {cosecha}")
# Leer dataframe

if (path.exists(rinde))&(path.exists(resumen)):


    
    df_rinde = pd.read_csv(rinde)
    df_resumen = pd.read_csv(resumen)

    c_esperada = df_resumen.loc[0,'C_esp_kg_h']
    Perd_capa = df_resumen.groupby('Capa').agg(Perdidas=('Perd_kg_h','sum'),Poc_=('Porc_Perd','sum')).reset_index().sort_values(by='Perdidas',ascending = False)
    capas = Perd_capa['Capa'].to_list()

    cps = capas.copy()
    # Opciones por capa:
    capas.append('Resumen')
    capa = st.selectbox("Cuál capa desea revisar?",capas)
    if capa == 'Resumen':
        Labels = list(Perd_capa.loc[:,'Capa'].values)
        labels = []
        for l in Labels:
            labels.append(l.split('_')[0])

        # Perdidas Rinde Global
        #====================================================

        var=['Rinde. Prom. kg/ha','% Per. Global','Calidad Global','Perd. Global kg/ha','Perd. USD/ha','% Ajuste']
        por_perdida = 0
        ajuste = 0.0
        for cp in cps:
            Capa = df_resumen[df_resumen['Capa']==cp].copy()
            por_perdida += Capa['Porc_Perd'].sum()
            ajuste += Capa['Ajuste'].mean().round(2)
        ajuste = round(ajuste/len(cps),2)
        Cal_global = round(100-por_perdida,2)
        per_global = round(df_resumen['Perd_kg_h'].sum(),2)

        Perd_USD = round(per_global*0.27,2)
        values = [round(c_esperada,2),por_perdida,Cal_global,per_global,Perd_USD,ajuste]
        rinde_g = pd.DataFrame({'Variable':var,'Valor':values})

        # A los Graficos
        #=================================================================

        fig = make_subplots(rows=2, cols=2,specs=[[{"type": "pie"}, {"type": "table"}],[{"type": "table"},{"type": "table"}]],subplot_titles=("", "", "Perdida por capa", "Resumen General"))
        fig.add_trace(go.Pie(labels=labels,values=list(Perd_capa['Perdidas'].values),
            textinfo='label+percent', pull=[0.2, 0.2, .3, 0.1,0],insidetextorientation='radial'),
              row=1, col=1)
        fig.add_trace(go.Table(header=dict(values=Perd_capa.columns.to_list(),font=dict(color='Green', size=14)),
                 cells=dict(values=[list(Perd_capa[x].values) if i==0 else  list(Perd_capa[x].values.round(2)) for i,x in enumerate(Perd_capa.columns.to_list())])),
                 row=2, col=1)

        fig.add_trace(go.Table(header=dict(values=rinde_g.columns.to_list(),font=dict(color='Green', size=14),line = dict(color='rgb(50, 50, 50)'),
            fill = dict(color='#d562be')),cells=dict(values=[list(rinde_g[x].values) for x in rinde_g.columns.to_list()],
            line_color='darkslategray',fill=dict(color=['paleturquoise', 'white']),align=['left', 'center'])),row=2, col=2)

        fig.update_annotations(font_size=fontsize)

        fig.update_layout(height=700, width=1000,title_text="Perdidas Generales",showlegend=False,
                 title_font_size=fontsize,title_font_color='Green',title_font_family='Titillium Web')

        st.write(fig)

    elif capa in cps:
        df_capa = df_resumen[df_resumen['Capa']==cps[capas.index(capa)]].copy()
        Capa = df_capa[['Variable','Ajuste','Porc_Perd','Perd_kg_h']].copy()

        # Buscando los Rangos
        #===================================================================
        Rangos = df_capa[['Variable','R_Ini','R_Fin','Ajuste']].copy()

        # Rinde Global para la capa:
        #===================================================================
        var=['Rinde. Prom. kg/ha','% Per. Global','Calidad Global','Perd. Global kg/ha','Perd. USD/ha','% Ajuste']
        values = [c_esperada,Capa['Porc_Perd'].sum().round(2),round(100-Capa['Porc_Perd'].sum().round(2),2),Capa['Perd_kg_h'].sum().round(2),round(Capa['Perd_kg_h'].sum().round(2)*0.27,2),Capa['Ajuste'].mean().round(2)]
        rinde_g = pd.DataFrame({'Variable':var,'Valor':values})

        # Perdidas Globales -- Capa Siembra
        #============================================================================================================
        fig=make_subplots(rows=2, cols=2,specs=[[{'type':"table"},{"type": "pie"}],[{"type": "table"},{'type':"table"}]],subplot_titles=("Perdidas por Variable", "", "Resumen", "Rango Sugerido"))
        fig.add_trace(go.Table(header=dict(values=Capa.columns.to_list(),font=dict(color='Green', size=14)),cells=dict(values=[list(Capa[x].values) if i==0 else  list(Capa[x].values.round(2)) for i,x in enumerate(Capa.columns.to_list())])),row=1, col=1)
        fig.add_trace(go.Table(header=dict(values=rinde_g.columns.to_list(),font=dict(color='Green', size=14),line = dict(color='rgb(50, 50, 50)'),
            fill = dict(color='#d562be')),cells=dict(values=[list(rinde_g[x].values) for x in rinde_g.columns.to_list()],
            line_color='darkslategray',fill=dict(color=['paleturquoise', 'white']),align=['left', 'center'])),row=2, col=1)
        fig.add_trace(go.Pie(labels=Capa.loc[:,'Variable'],values=list(Capa['Porc_Perd'].values),textinfo='label+percent',pull=[0.1, 0.1, .3, 0,0],insidetextorientation='radial'),row=1, col=2)
        fig.add_trace(go.Table(header=dict(values=Rangos.columns.to_list(),font=dict(color='Green', size=14)),cells=dict(values=[list(Rangos[x].values) for x in Rangos.columns.to_list()])),row=2, col=2)

        fig.update_annotations(font_size=fontsize)
        fig.update_layout(height=600, width=900, title_text='Capa: '+capa,showlegend=False,title_font_size=fontsize+2,
            title_font_color='Green',title_font_family='Titillium Web')
        st.write(fig)
        #st.write(rinde_g)
else: 
    st.error('Error... file rinde/resumen not found...', icon="🚨")



# # Filter data for renge date and distrit
# date_ini = pd.to_datetime(date_ini, format="%Y-%m-%d") # Conertir a DateTime
# date_end = pd.to_datetime(date_end, format="%Y-%m-%d")

# df["DATE"] = pd.to_datetime(df["DATE"] , infer_datetime_format=True)

# df_acc = df[(df['BOROUGH']==selected_dist)&(df['DATE']>=date_ini)&(df['DATE']<=date_end)]
# df_acc.reset_index(drop = True, inplace = True)

# if df_acc.shape[0]>0:
#     total = [df_acc[col].sum() for col in ['PERSONS INJURED','PERSONS KILLED','PEDESTRIANS INJURED','PEDESTRIANS KILLED','CYCLISTS INJURED','CYCLISTS KILLED','MOTORISTS INJURED','MOTORISTS KILLED']]

#     per_acc = total/sum(total)*100
#     per_acc = per_acc.round(2)

#     col1,col2 = st.columns(2)

#     df_ = pd.DataFrame({'Event':['PER-INJURED','PER-KILLED','PED-INJURED','PED-KILLED','CYC-INJURED','CYC-KILLED','MOT-INJURED','MOT-KILLED'],
#                  'Perc': per_acc})

#     df_.set_index('Event',inplace=True)

#     fig, ax = plt.subplots()

#     # declaring exploding pie
#     explode = [0.2, 0.2,  0.2,  0.2,  0.2, 0.2, 0.2, 0.2]

#     # define Seaborn color palette to use
#     sns.set_theme(palette="dark", font="serif", font_scale= 0.5)
  
#     # plotting data on chart
#     ax.pie(df_['Perc'], labels=df_.index, explode=explode, autopct='%.0f%%')

 
    
#     # Add Plot Title
#     f_ini = str(date_ini.year)+'/'+str(date_ini.month)
#     f_end = str(date_end.year)+'/'+str(date_end.month)
#     ax.set_title(f'Percentage of persons INJURED/KILLED in district {selected_dist}',fontsize=11,
#              loc='left', pad = 20)
#     fig.suptitle(f'On dates {f_ini} - {f_end}', y=1, fontsize=9)

#     st.pyplot(fig)

# st.button("Re-run")

