# -*- coding: utf-8 -*- #

import json
import pandas as pd
import os

def read_preprocessing_trains():
    ''' Extraemos los años diferentes a 2017, 2018 y 2019
        y eliminamos los tipos de viajes(filas) que no vamos a 
        utilizar '''
    total_rows = []
    new_dataframe = pd.DataFrame()

    dataframe = pd.read_excel(f'{os.path.abspath("..")}\\RawData\\viajes.xlsx', sheet_name='ViajerosTransportados')
    #print(dataframe)
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
    
    write_to_csv(new_dataframe, 'trenes')
    return new_dataframe

def read_unify_calendar():
    ''' Creamos los calendarios y los unificamos, tambien les añadimos la columna de año'''
    calendar_17 = pd.read_json(f'{os.path.abspath("..")}\\RawData\\calendario2017.json')
    calendar_18 = pd.read_json(f'{os.path.abspath("..")}\\RawData\\calendario2018.json')
    calendar_19 = pd.read_json(f'{os.path.abspath("..")}\\RawData\\calendario2019.json')
    
    # Para cada calendario añadimos la columna anio (año)
    t17 = []
    for i in range(0, len(calendar_17.index)):
        t17.append(2017)
    calendar_17['Anio'] = t17

    t18 = []
    for i in range(0, len(calendar_18.index)):
        t18.append(2018)
    calendar_18['Anio'] = t18

    t19 = []
    for i in range(0, len(calendar_19.index)):
        t19.append(2019)
    calendar_19['Anio'] = t19
    
    # Unificamos los 3 dataframes de calendario para formar un unico calendario
    full_calendar = pd.concat([calendar_17, calendar_18, calendar_19])
   
    # Escribimos este calendario en un csv para solamente tener que leerlo a modo de dataframe con pad
    write_to_csv(full_calendar, 'calendario')
    return full_calendar

def write_to_csv(dataframe, nombre):
    dataframe.to_csv(f'{os.path.abspath("..")}\\ProcessedData\\{nombre}.csv')

def main():
    train = read_preprocessing_trains()
    calendar = read_unify_calendar()
    #print(calendario)
    #print(trenes)
    # Como se crea una tarjeta de datos??
    # print(pd.concat([trenes,calendario]))

if __name__=='__main__':
    main()
   