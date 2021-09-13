import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import lasio
import io


st.title("Well Logging Tool")
st.sidebar.title("Menu")
#archivo_las=lasio.read("LGAE-040.las")
#df=archivo_las.df()
archivo_las = st.sidebar.file_uploader("Cargar archivo LAS" , key=None)
        
if archivo_las is None:
	st.write("Suba un archivo con extensión .las")
if archivo_las is not None:
	bytes_data = archivo_las.read()
	str_io = io.StringIO(bytes_data.decode('Windows-1252'))
	las_file = lasio.read(str_io)
	df = las_file.df()
	seleccion_columnas=df.columns
	cant_log=len(seleccion_columnas)
	prof_max=df.index[-1]
	prof_min=df.index[0]





#archivo_cargado = st.sidebar.file_uploader("Cargar archivo LAS" , type=['.las', '.LAS'], key=None)






opciones_inicio=st.sidebar.radio("Seleccione una opción",["Inicio","Información de Data","Análisis de Data","Visualización de Data"])
if opciones_inicio=="Inicio":
	with st.expander("Instrucciones"):
		st.write("Cargue el archivo LAS a analizar en el menu desplegable ")
		st.write("Dirijase a **Análisis de Data** para obtener estadísticas de las curvas. ")
		st.write("Dirijase a **Visualización de de Data**, seleccione las curvas a graficar con sus respectivos colores.")
		st.write("Seleccionar los límites de la capa a graficar.")


	with st.expander("Descripción"):
		st.write("**Información de Data** ")
		st.write("DataFrame extraído del archivo LAS.")
		st.write("DataFrame filtrado con curvas seleccionadas por el usuario.")
		st.write("Datos del Pozo. ")
		st.write("**Análisis de Data**")
		st.write("Estadísticas de curvas seleccionadas por el usuario.")
		st.write("DataFrame filtrado por capas.")
		st.write("**Visualización de Data**")
		st.write("Graficas de Curvas seleccionadas en capas definidas por el usuario.")



	st.info("Aplicación creada por Pablo I. Jarrín - Ingeniero en Petróleos - paisjarr@espol.edu.ec - +593990708371")

		


if opciones_inicio=="Información de Data":
	st.write("Información de Data")
	with st.expander("DataFrame"):
		st.write(df)
		filtro=st.multiselect("Seleccione curvas a filtrar",seleccion_columnas)
		df_filtrado=df[filtro]
		st.write(df_filtrado)

	with st.expander("Información del Registro"):

		nombre_pozo=las_file.header["Well"].WELL.value
		pais = las_file.header['Well'].COUNT.value
		campo = las_file.header['Well'].FLD.value
		provincia = las_file.header['Well'].PROV.value
		compania = las_file.header['Well'].COMP.value

		columna1,columna2=st.columns(2)
		with columna1:
			st.write('Nombre pozo:', nombre_pozo)
			st.write('Campo:', campo)
			st.write('Compania:', compania)
			st.write('Tope de Intervalo:', prof_min)
		with columna2:
			st.write('Pais:', pais)
			st.write('Provincia:', provincia)
			st.write('Curvas Registradas:', cant_log)
			st.write('Base de Intervalo:', prof_max)

if opciones_inicio=="Análisis de Data":

	with st.expander("Estadisticas"):
		filtro=st.multiselect("Seleccione curvas a filtrar",seleccion_columnas)
	
		if bool(filtro) == True:
			df_filtrado=df[filtro]
			st.write(df_filtrado)
			df_estadisticas =df_filtrado.describe()
			st.write(df_estadisticas)

	with st.expander("Información del Registro"):
		column1,column2=st.columns(2)
		if bool(filtro)==True:
			with column1:
				prof_max=df.index[-1]
				prof_min=df.index[0]
				ingreso_numero1=st.number_input("Ingrese límite superior de Capa 1",min_value=prof_min,max_value=prof_max,value=prof_min)
				ingreso_numero2=st.number_input("Ingrese límite inferior de Capa 1",min_value=prof_min,max_value=prof_max,value=prof_max)
				st.write(df_filtrado[ingreso_numero1:ingreso_numero2])
			with column2:
				prof_max=df.index[-1]
				prof_min=df.index[0]
				ingreso_numero3=st.number_input("Ingrese límite superior de Capa 2",min_value=prof_min,max_value=prof_max,value=prof_min)
				ingreso_numero4=st.number_input("Ingrese límite inferior de Capa 2",min_value=prof_min,max_value=prof_max,value=prof_max)	
				st.write(df_filtrado[ingreso_numero3:ingreso_numero4])

if opciones_inicio=="Visualización de Data":
	st.write("Visualización de Data")
	filtro=seleccion_columnas
	filtro=st.multiselect("Seleccione al menos 2 curvas a filtrar",seleccion_columnas)
	df_filtrado=df[filtro]
	colores=["Black","Grey","Blue","Cyan","Red","Green","Yellow","Magenta","Pink","Violet","Orange","Brown","Beige","Gold"]
	colors=st.multiselect("Seleccione color de las curvas en orden correspondiente",colores)
	st.write(len(filtro))
	#df_filtrado=df_filtrado.dropna(subset=filtro,axis=0,how="any")



	column1,column2=st.columns(2)
	prof_min=df.index[0]
	prof_max=df.index[-1]
	with column1:
		ingreso_numero1=st.number_input("Ingrese límite superior de Capa",min_value=prof_min,max_value=prof_max,value=(prof_min+prof_max)/2)
	with column2:
		ingreso_numero2=st.number_input("Ingrese límite inferior de Capa",min_value=prof_min,max_value=prof_max,value=prof_max)

	selfiltro=st.selectbox("Desea Filtrar valores nulos de las curvas selccionadas?",["Si","No"])

	df_filtrado2=df_filtrado[ingreso_numero1:ingreso_numero2]
	st.write("Data Frame")


	if selfiltro=="Si":
		df_filtrado2=df_filtrado2.dropna(subset=filtro,axis=0,how="any")



	

	st.write(df_filtrado2)
	curvas=len(filtro)
	df_filtrado2["Depth"]=df_filtrado2.index


	#Para Graficas siempre iniciando desde un numero multiplo de 10
	if df_filtrado2.index[0]>ingreso_numero1:
		ingreso_numero1=df_filtrado2.index[0]
	if ingreso_numero1%10 != 0:
		ingreso_numero1=ingreso_numero1 - ingreso_numero1%10


	if len(filtro)>1:	


		f,ax=plt.subplots(nrows=1,ncols=curvas,figsize=(10,(ingreso_numero2-ingreso_numero1)/5))
		major_ticks = np.arange(ingreso_numero1, ingreso_numero2, 5)
		minor_ticks = np.arange(ingreso_numero1, ingreso_numero2, 1)
		for i,log,color in zip(range(curvas),filtro,colors):
			ax[i].plot(df_filtrado2[log],df_filtrado2["Depth"],color=color)
			ax[i].invert_yaxis()

			ax[i].xaxis.set_label_position('top')
			ax[i].set_xlabel(filtro[i])


		# Major ticks every 20, minor ticks every 5


			ax[i].set_yticks(major_ticks)
			ax[i].set_yticks(minor_ticks, minor=True)


			ax[i].grid(which='major', alpha=0.5)
			ax[i].grid(which='minor', alpha=0.2)
			ax[i].tick_params(axis='y',labelright=False,labelleft=False)



		ax[0].set_ylabel("Profundidad")
		ax[0].tick_params(axis='y',labelleft=True)
		ax[-1].tick_params(axis='y',labelright=True)
		st.pyplot(f)




	#f2,ax=plt.subplots(figsize=(10,10))
	#for i,log,color in zip(range(curvas),filtro,colors):
	#	ax.plot(df_filtrado2[log],df_filtrado2["Depth"],color=color)
	#	ax.invert_yaxis()
	#	ax.grid()
	#st.pyplot(f2)
	


