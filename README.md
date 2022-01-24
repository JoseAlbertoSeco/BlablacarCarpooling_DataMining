# Blablacar Carpooling
El retoCajamar Carpooling nos presenta los datos obtenidos de la aplicación Blablacar,app utilizada por los usuarios para realizar viajes a bajo coste en vehículos de particulares.
En este proyecto se sigue el proceso KDD para extraer información de grandes volumenes de datos.

# Objetivos
**Objetivo principal**:

Como principal objetivo vamos a extraer los  viajes realizados en la población Española, estos viajes junto con los días festivos a nivel nacional y de autonomía nos servirán para extraer conclusiones sobre los desplazamientos realizados en vacaciones y poder inferir sobre comportamientos sociales futuros, como poder ofertar más viajes a una determinada ciudad en una festividad.  Primero realizaremos la estimación por las provincias de Castilla-La Mancha y Andalucía.

**Objetivo secundario**:

Realizar la comparativa viajeros trenes/blablacar, usando distintitos medios de transporte, por lo tanto, podríamos discutir si se estan ofertando unos recursos no utilizados. Para este objetivo parcial necesitaremos los trenes y demás medios ofertados junto con los viajes blablacar.

# Empecemos :rocket:

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo.

## Análisis de archivos

En la rama **main** nos podemos encontrar todos los archivos pertenecientes a este proyecto con la siguiente estructura:

![image](https://drive.google.com/uc?export=view&id=1wXv9-gwfLIteeZG-DDGtHnLRQPilMbL4)

* Como se puede observar se ha seguido la estructura de proyecto [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)

## Pre-requisitos

Las librerías necesarias para la correcta ejecución del proyecto se encuentran en el archivo [requirements.txt](https://github.com/JoseAlbertoSeco/MineriaDatos/blob/main/requirements.txt).
Para instalar las dependencias:

```python
pip install -r requirements.txt
```
Es posible que su sistema use el instalador **pip3**, en cuyo caso la instalación se realizaría de la siguiente manera:

```python
pip3 install -r requirements.txt
```

Una vez instaladas las diferentes librerías se deberán descargar algunos datos que no estan incluidos en este repositorio por contener un tamaño excesivo.
Estos datos han de ser incluidos en una carpeta drive llamada Datos.
* [DATOS_BLABLACAR](https://drive.google.com/file/d/1X3OAsvt03Rv9cEcW0KOcrA6ZjwBIV94Q/view?usp=sharing): Rawdata con los datos del blablacar, han de ser introducidos en la carpeta *data/raw*
* [blablacar_basic](https://drive.google.com/file/d/1XYfVdHCcOCy-p40fjcKi0b6N6x6z7awh/view?usp=sharing): Dataframe de DATOS_BLABLACAR preprocesado.
* [df_trenes](https://drive.google.com/file/d/1uOb10sr_1bdtHfCOpHUQQZe6engoqawz/view?usp=sharing): Tarjeta de datos de los trenes, incluir en data/processed.

## Modo de uso
- Primero se realizo un análisis básico de datos para encontrar diferentes problemáticas, se puede encontrar en el archivo *problems_analysis* de la carpeta *notebooks*.
- Ejecutamos el preprocesado básico de datos, para ello utilizaremos los archivos de la carpeta *src/* en el siguiente orden:

- Para empezar nos ubicaremos en la carpeta *src*.

Archivo en el que preprocesamos los datos del archivo *DATOS_BLABLACAR.txt*
```python
python3 features/preprocesing_blablacar.py
```

Archivo en el que preprocesamos los datos que se encuentran en la carpeta *data/raw*.
```python
python3 features/preprocesing_external_data.py
```

Archivo en el que preprocesamos diversos datos de dos dataframes obtenidos tras la ejecución de los archivos anteriores.
```python
python3 features/preprocesing.py
```

A continuación unificamos todos estos archivos en el *colab* [GeolocalizacionProvincial](https://github.com/JoseAlbertoSeco/MineriaDatos/blob/main/notebooks/GeolocalizacionProvincial.ipynb) 
que podemos encontrar en la carpeta *notebooks*, en el que realizamos dos tarjetas de datos. 
Estas tarjetas de datos se corresponden a los dataframes [df_AndaluciaLocalizado](https://github.com/JoseAlbertoSeco/MineriaDatos/blob/main/data/processed/df_AndaluciaLocalizado.csv)
y [df_CLMLocalizado](https://github.com/JoseAlbertoSeco/MineriaDatos/blob/main/data/processed/df_CLMLocalizado.csv) que encontramos en la carpeta *data/processed*.

- En el archivo *GráficasTrasPreprocesado* que encontramos en la carpeta *notebooks* podemos encontrarnos dos gráficas con el total de viajes interprovinciales de _Castilla-La Mancha_ y _Andalucía_

El archivo *colab* [TrenesPreprocesado](https://github.com/JoseAlbertoSeco/BlablacarCarpooling_DataMining/blob/main/notebooks/TrenesPreprocesado.ipynb) se encuentra la obtención de la tarjeta de datos de los trenes, el archivo generado no se ha podido almacenar en GitHub debido a que pesa más de 25MB.

## Lineas de trabajo.
Las lineas de trabajo desarrolladas se encuentran en la carpeta *notebooks*. Estos archivos son:
* Regresion
* Clasificacion_Binaria
* Clasificacion_Multiobjetivo
* ComparacionTransporte

## Construido con :keyboard:

* Python3: para preprocesado de datos demasiado pesados
* Colab: para obtener la tarjeta de datos, pattern y knowledge (KDD), y muestra de datos.

## Autores :pencil:

* [María Blanco Gónzalez-Mohíno](https://github.com/MariaBlancoGonzalez/)
* [José Alberto Seco Sánchez-Camacho](https://github.com/JoseAlbertoSeco/)
* [Pablo Velasco Crespo](https://github.com/PabloVelascoCrespo/)
