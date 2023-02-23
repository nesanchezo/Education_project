import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Dashboard",
)

#---------------------------------#
# Page layout
## Page expands to full width
#st.set_page_config(layout="wide")
#---------------------------------#

st.write("""
# Piloto Dashboard Colegios - secondLabel!
""")

#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** plotly, pandas, streamlit, numpy, matplotlib, seaborn
Se presenta la predicción de como sera el rendimiento del estudiantes en el 
siguiente trimestre académico.
""")

df = pd.read_csv('data_model.csv')
#df = df[df.fecha=='2021-12-01']

fechas = df.fecha.unique()
fecha = st.sidebar.selectbox(
    'Seleccione fecha a visualizar',fechas)

st.write('You selected:', fecha) 

if fecha=='GENERAL':
	df_grado = df
else:
	df_grado = df[df.fecha==fecha]


grados = ['GENERAL', 'PRIMERO', 'SEGUNDO', 'TERCERO', 'CUARTO', 'QUINTO', 'SEIS',
			'SIETE', 'OCHO', 'NUEVE','DIEZ',  'ONCE']
grado = st.sidebar.selectbox(
    'Seleccione grado a visualizar',grados)

st.write('You selected:', grado) 

if grado=='GENERAL':
	df_grado = df_grado
else:
	df_grado = df_grado[df_grado.segment==grado]


df_pie = df_grado.groupby('secondLabel',as_index=False).nombre.count()

col1, col2, col3 = st.columns(3)

try:
	col1.metric('RedFlag', int(df_pie[df_pie.secondLabel=='RedFlag'].nombre.iloc[0]))
except:
	col1.metric('RedFlag', '0')
	df_pie=df_pie.append({'secondLabel' : 'RedFlag' , 'nombre' : 0} , ignore_index=True)
try:
	col2.metric('OrangeFlag', int(df_pie[df_pie.secondLabel=='OrangeFlag'].nombre.iloc[0]))
except:
	col2.metric('OrangeFlag', '0')
	df_pie=df_pie.append({'secondLabel' : 'OrangeFlag' , 'nombre' : 0} , ignore_index=True)
try:
	col3.metric('GreenFlag', int(df_pie[df_pie.secondLabel=='GreenFlag'].nombre.iloc[0]))
except:
	col3.metric('GreenFlag', '0')
	df_pie=df_pie.append({'secondLabel' : 'GreenFlag' , 'nombre' : 0} , ignore_index=True)

fig1 = px.pie(df_pie, values='nombre', names='secondLabel', title='Alertas para estudiantes')
st.plotly_chart(fig1)

fig2 = px.bar(df_pie, x='secondLabel', y='nombre', title='Alertas para estudiantes')
st.plotly_chart(fig2)


materias = ['Ciencias naturales', 'Ciencias sociales', 'Educación artística',
'Educación física', 'Lengua castellana', 'Idioma extranjero', 'Matemáticas', 
'Sensibilización Pedagógica', 'Tecnología e informática', 'Humanidades']

dict_materias = {'Ciencias naturales':'Ciencias naturales-nota_p4', 'Ciencias sociales':'Ciencias sociales-nota_p4', 'Educación artística':'Educación artística-nota_p4',
'Educación física':'Educación física-nota_p4', 'Lengua castellana':'Lengua castellana-nota_p4', 'Idioma extranjero':'Idioma extranjero-nota_p4',
'Matemáticas':'Matemáticas-nota_p4', 'Sensibilización Pedagógica':'Sensibilización Pedagógica-nota_p4', 'Tecnología e informática':'Tecnología e informática-nota_p4',
'Humanidades':'Humanidades-nota_p4'}

flags = ['GreenFlag','OrangeFlag', 'RedFlag']
flag = st.selectbox(
    'Escoja una bandera a visualizar',flags)

st.write('You selected:', flag)

df_grado_flags = df_grado[df_grado.secondLabel==flag].nombre

st.table(df_grado_flags)

tab1, tab2, tab3 = st.tabs(['GreenFlag','OrangeFlag', 'RedFlag'])

with tab1:
   st.header("GreenFlag")
   df_grado_flags2 = df_grado[df_grado.secondLabel=='GreenFlag'].nombre
   st.table(df_grado_flags2)

with tab2:
   st.header("OrangeFlag")
   df_grado_flags2 = df_grado[df_grado.secondLabel=='OrangeFlag'].nombre
   st.table(df_grado_flags2)

with tab3:
   st.header("RedFlag")
   df_grado_flags2 = df_grado[df_grado.secondLabel=='RedFlag'].nombre
   st.table(df_grado_flags2)
