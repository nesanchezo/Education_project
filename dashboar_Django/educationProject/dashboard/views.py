from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objects as go

import pandas as pd
import pickle5 as pickle
import xgboost as xgb
# Create your views here.

# -----------load data----------------
df = pd.read_csv('data/data_model.csv')

with open('data/model.pickle', 'rb') as f:
    pred_model = pickle.load(f)


grados = ['GENERAL', 'PRIMERO', 'SEGUNDO', 'TERCERO', 'CUARTO', 'QUINTO', 'SEIS',
			'SIETE', 'OCHO', 'NUEVE','DIEZ',  'ONCE']
#--------------------------------------


#----------fuctions predict-------------------

def predictionLabel(df,model,fecha='2021-12-01'):
    df.set_index('nombre',inplace=True)  
    df = df[df.fecha==fecha].drop(['fecha','firstLabel','secondLabel'],axis=1)
    segment = pd.get_dummies(df['segment'], drop_first = True)
    df2 = df['segment']
    df = df.drop(['segment'], axis = 1)
    df = pd.concat([df,segment], axis = 1)
    df['secondLabel']= model.predict(df)
    df['segment'] = df2
    df['secondLabel'] = df['secondLabel'].replace([0,1,2,3,4],['GreenFlag', 'WhiteFlag', 'YellowFlag', 'OrangeFlag', 'RedFlag'])
    return df

def dfPie(df,grado):
	if grado=='GENERAL':
		df = df
	else:
		df = df[df.segment==grado]
	df = df.reset_index()
	df_pie = df.groupby('secondLabel',as_index=False).nombre.count()
	return df_pie

def dfPie2(df,grado):
	if grado=='GENERAL':
		df = df
	else:
		df = df[df.segment==grado]
	df = df.reset_index()
	return df

df_grado = predictionLabel(df,pred_model)


grados = ['GENERAL', 'PRIMERO', 'SEGUNDO', 'TERCERO', 'CUARTO', 'QUINTO', 'SEIS',
			'SIETE', 'OCHO', 'NUEVE','DIEZ',  'ONCE']

def tarjetas(df_pie):
	try:
		numRedFlag = int(df_pie[df_pie.secondLabel=='RedFlag'].nombre.iloc[0])
	except:
		numRedFlag = 0
		df_pie=df_pie.append({'secondLabel' : 'RedFlag' , 'nombre' : 0} , ignore_index=True)
	try:
		numOrangeFlag = int(df_pie[df_pie.secondLabel=='OrangeFlag'].nombre.iloc[0])
	except:
		numOrangeFlag = 0
		df_pie=df_pie.append({'secondLabel' : 'OrangeFlag' , 'nombre' : 0} , ignore_index=True)
	try:
		numGreenFlag = int(df_pie[df_pie.secondLabel=='GreenFlag'].nombre.iloc[0])
	except:
		numGreenFlag = 0
		df_pie=df_pie.append({'secondLabel' : 'GreenFlag' , 'nombre' : 0} , ignore_index=True)
	return numRedFlag, numOrangeFlag, numGreenFlag, df_pie

def dashboard(request):
	global categoria_seleccionada
	categorias = grados
	categoria_seleccionada = request.GET.get('categoria')
	#url_dfRedFlag = reverse('dfRedFlag', args=[categoria_seleccionada])
	df_pie = dfPie(df_grado,categoria_seleccionada)
	numRedFlag, numOrangeFlag, numGreenFlag, df_pie = tarjetas(df_pie)
	#df_GreenFlag = df_grado[df_grado.secondLabel == 'GreenFlag'].reset_index().nombre
	#df_OrangeFlag = df_grado[df_grado.secondLabel == 'OrangeFlag'].reset_index().nombre
	#df_RedFlag = df_grado[df_grado.secondLabel == 'RedFlag'].reset_index().nombre
	graphs = px.pie(df_pie, values='nombre', names='secondLabel', title='Alertas para estudiantes grado ' + categoria_seleccionada)
	graphs2 = px.bar(df_pie, x='secondLabel', y='nombre', title='Alertas para estudiantes grado ' + categoria_seleccionada)
	plot_div = plot({'data': graphs}, output_type='div')
	plot_div2 = plot({'data': graphs2}, output_type='div')
	resultados = {'plot_div': plot_div,'plot_div2': plot_div2,'categorias': categorias,'numRedFlag':numRedFlag,'numOrangeFlag':numOrangeFlag,'numGreenFlag':numGreenFlag}
	return render(request,'dashboard.html',resultados)

def dfRedFlag(request):
	df_grado2 = dfPie2(df_grado,categoria_seleccionada)
	df_RedFlag = df_grado2[df_grado2.secondLabel == 'RedFlag'].reset_index().nombre.to_frame()
	df_RedFlag_html = df_RedFlag.to_html(classes='table table-striped')
	resultados = {'df_RedFlag_html': df_RedFlag_html}
	return render(request,'dfRedFlag.html',resultados)

def dfOrangeFlag(request):
	df_grado2 = dfPie2(df_grado,categoria_seleccionada)
	df_OrangeFlag = df_grado2[df_grado2.secondLabel == 'OrangeFlag'].reset_index().nombre.to_frame()
	df_OrangeFlag_html = df_OrangeFlag.to_html(classes='table table-striped')
	resultados = {'df_OrangeFlag_html': df_OrangeFlag_html}
	return render(request,'dfOrangeFlag.html',resultados)

def dfGreenFlag(request):
	df_grado2 = dfPie2(df_grado,categoria_seleccionada)
	df_GreenFlag = df_grado2[df_grado2.secondLabel == 'GreenFlag'].reset_index().nombre.to_frame()
	df_GreenFlag_html = df_GreenFlag.to_html(classes='table table-striped')
	resultados = {'df_GreenFlag_html': df_GreenFlag_html}
	return render(request,'dfGreenFlag.html',resultados)
