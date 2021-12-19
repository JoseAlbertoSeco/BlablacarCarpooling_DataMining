#!/usr/bin/env python3

import json
import pandas as pd
import os
import geopandas as gpd
from geojson import dump

MESES = {'enero': '01', 'febrero': '02', 'marzo':'03',
        'abril': '04', 'mayo': '05', 'junio': '06',
        'julio': '07', 'agosto':'08', 'septiembre': '09',
        'octubre': '10', 'noviembre': '11', 'diciembre':'12'
        }

def write_to_csv(dataframe, nombre):
    #dataframe = dataframe.drop(dataframe.columns[[0]], axis='columns')
    dataframe.to_csv(f'{os.path.abspath("..")}/data/processed/{nombre}.csv', index = False)


def read_preprocessing_trains():
    ''' Extraemos los años diferentes a 2017, 2018 y 2019
        y eliminamos los tipos de viajes(filas) que no vamos a 
        utilizar '''
    total_rows = []
    new_dataframe = pd.DataFrame()

    dataframe = pd.read_excel(f'{os.path.abspath("..")}/data/raw/viajes.xlsx', sheet_name='ViajerosTransportados')
    total_rows = dataframe.index.values

    # Filas con las que nos queremos quedar
    rows_we_want = ['Transporte urbano','Urbano por metro','Transporte urbano regular por autobús', 
        'Transporte interurbano regular','Interurbano por autobús regular','Interurbano por ferrocarril','AVE']
    
    # Sacamos la fila de las fechas y la convertimos a lista
    date = dataframe.iloc[0, :]
    date.to_numpy().tolist().pop(0)

    # Creamos un nuevo dataframe en el que se cojen solo las columnas q queremos y las comparamos para ver q es
    # la correcta, si tenemos esa columna la metemos en el nuevo dataframe, una vez tenemos todas solo introducimos
    # la fecha de cada uno de los viajes por meses
    for i in rows_we_want:
        for j in total_rows:            
            if i in dataframe.iloc[j, 0:].values:
                new_dataframe[i] = dataframe.iloc[j, 0:]
            
    new_dataframe['Fecha'] = date
    
    # Quitar el nombre 'Unnamed' a las filas y lo sustituimos por un id incremental desde 0
    nombrar_filas = {}
    for i in range(len(new_dataframe.index)):
        nombrar_filas.update({i:i})

    new_dataframe.index = nombrar_filas

    new_dataframe = new_dataframe.drop(new_dataframe.index[[0]])

    print('\nDataframe sobre trenes generado')
    print(new_dataframe.head(3))
    write_to_csv(new_dataframe, 'trenes')

def get_date(date, anio):
    date = date.split()
    final_date = ''
    if len(date[0]) == 1:
        final_date += f'0{date[0]}/'
    else: 
        final_date += f'{date[0]}/'

    final_date += f'{MESES.get(date[2])}/{anio}'

    return final_date

def create_calendar_dataframe(json_file, anio):
    df = pd.DataFrame()
    for key, value in json_file.items():
        fecha = []
        for i in value:
            if i != 0:
                fecha.append(get_date(i, anio))
            else: 
                fecha.append('Laborable')
        df[f'{key}'] = fecha
    return df

def read_unify_calendar():
    ''' Creamos los calendarios y los unificamos, tambien les añadimos la columna de año'''

    calendar17 = open(f'{os.path.abspath("..")}/data/raw/Calendario2017.json')
    calendar17 = json.load(calendar17)
    calendar17 = create_calendar_dataframe(calendar17, '2017')

    calendar18 = open(f'{os.path.abspath("..")}/data/raw/Calendario2018.json')
    calendar18 = json.load(calendar18)
    calendar18 = create_calendar_dataframe(calendar18, '2018')

    calendar19 = open(f'{os.path.abspath("..")}/data/raw/Calendario2019.json')
    calendar19 = json.load(calendar19)
    calendar19 = create_calendar_dataframe(calendar19, '2019')
        
    full_calendar = pd.concat([calendar17, calendar18, calendar19])

    # Escribimos este calendario en un csv para solamente tener que leerlo a modo de dataframe con pandas
    print('\nDataframe sobre fechas generado')
    print(full_calendar.head(3))
    write_to_csv(full_calendar, 'calendario')


def comprobacion(df):
    # Ver que nombres no se encuentran en los dos dataframes
    bla = pd.read_csv(f'{os.path.abspath("..")}/data/processed/blablacar_basic.csv')

    origen = bla['ORIGEN'].tolist()
    destino = bla['DESTINO'].tolist()
    blabla_total = origen + destino
    blabla_total = list(set(blabla_total))

    total_municipios = df['Municipio'].tolist()
    total_municipios = list(set(total_municipios))

    diccionario = {item: True if item in total_municipios else False for item in blabla_total}

    municipios = []
    mano = 0
    repes = []
    for clave, valor in diccionario.items():
        if valor == False:
            for i in total_municipios:
                if clave in i and clave not in repes:
                    repes.append(clave)
                    mano += 1
                    municipios.append(clave)

    f = open (f'{os.path.abspath("..")}/data/interim/ciudades_no_españolas_extraidas.txt', "a")
    for i in municipios:
        f.write(i + '\n')
    f.close()

def preprocessing_coordinates():
    # Cargar la capa temática
    natalidad = f'{os.path.abspath("..")}/data/raw/natalidad.geojson'
    localizacion = gpd.read_file(natalidad)
    localizacion = localizacion.drop(['CC_2', 'NAT2018'], axis=1)
    print('\nDataframe sobre coordenadas generado')
    print(localizacion.head(3))
    with open(f'{os.path.abspath("..")}/data/processed/geolocalizaciones.geojson', 'w') as f:
        dump(localizacion, f)


def preprocessing_village():

    xls = pd.ExcelFile(f'{os.path.abspath("..")}/data/raw/municipios-provincia.xls') #use r before absolute file path 

    sheetX = xls.parse(0) #sheet
    sheetX = sheetX.iloc[:,[1,6,8]]

    # Nombre que empiezan por " (comilla dobles), los cuales se llaman diferente
    # Se guardan en un txt para tenerlo almacenado

    x = sheetX[sheetX['Municipio'].str.contains(",", case=False)]

    nombres = x.index.tolist()

    # Creación del dataframe que vamos a concatenar despues.
    # Es el df con los nombres bien puestos
    new_df = pd.DataFrame()
    new_df['Municipio'] = None
    new_df['Autonomía'] = None
    new_df['Provincia'] = None
    
    siguiente = False
    for i in x.Municipio.values:
        # Puntero a la lista del tipo: [Granja, La]
        pointer = 0

        for x in i.split():
            if x[-1] == ',':
                # Flag 
                siguiente = True

            if siguiente:                
                cadena_final = ''

                # Cadena entera sin la coma
                withoutcoma = i.replace(',', "")
                splitted = withoutcoma.split()

                # Despues de la coma
                cadena = splitted[pointer+1:len(splitted)]

                # Pasar de list a cadena lo que queremos concatenar
                cadena_final = " ".join(map(str, cadena)) 
                to_concat = " ".join(map(str, splitted[0:pointer+1]))
                cadena_final = cadena_final + " "+to_concat

                # Creamos una fila que metemos en el nuevo diccionario
                fila = sheetX[sheetX['Municipio'] == i] # Fila
                autonomia = fila['Autonomía'].to_numpy().tolist()[0] # Valor
                provincia = fila['Provincia'].to_numpy().tolist()[0] # Valor

                # Introducir valores ene l nuevo diccionario
                nueva_fila = { 'Municipio': cadena_final, 'Autonomía': autonomia, 'Provincia':provincia} # creamos un diccionario
                new_df = new_df.append(nueva_fila, ignore_index=True) # Introduciendo disccionario en el nuevo dataframe

                siguiente = False
                continue
            pointer += 1

    # Extraigo las filas que son del tipo "Granja, La"
    sheetX = sheetX.drop(nombres, axis=0)
    # Meto esas filas bien puestas
    sheetX = pd.concat([sheetX, new_df])

    comprobacion(sheetX)
    print('\nDataframe sobre municipios generado')
    print(sheetX.head(3))
    write_to_csv(sheetX, 'ccaa')

def main():
    print('Preprocesando datos externos... \nGenerando dataframes...')
    read_preprocessing_trains()
    read_unify_calendar()
    preprocessing_village()
    preprocessing_coordinates()

if __name__=='__main__':
    main()