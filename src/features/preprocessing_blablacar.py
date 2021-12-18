#!/usr/bin/env python3

import pandas as pd
import os
import json

''' Preprocesamiento básico de datos: DATOS_BLABLACAR.txt 

    Sólo tomamos los viajes que tienen más de 0 plazas confirmadas, y mas de 0 ofertadas.

    También obtenemos sólo los viajes realizados en territorio español

    El dataframe final se encuentra en la carpeta 'ProcessedData' con el nombre de 'blablacar'
'''

def preprocesing():
    blabla_data = pd.read_csv(f'{os.path.abspath("..")}/RawData/DATOS_BLABLACAR.txt', sep = "|")

    new_blabla = blabla_data[blabla_data['PAIS'] == 'es']

    new_blabla = new_blabla[new_blabla['ASIENTOS_OFERTADOS'] != 0]
    new_blabla =  new_blabla[new_blabla['ASIENTOS_CONFIRMADOS'] != 0]
    new_blabla = new_blabla.drop(['IMP_KM'], axis=1)

    portugal_cities = pd.read_excel(f'{os.path.abspath("..")}/RawData/portugal.xlsx')

    # Quitar nulos
    portugal_cities.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

    cities =  portugal_cities[['Municipios (concelhos)']]
    capitals = portugal_cities[['Ciudad']]
    cities = cities.to_numpy().tolist()
    capitals = capitals.to_numpy().tolist()
    lista = []

    lista = []
    for i in cities:
        lista.append(i[0])

    for i in capitals:
        if i[0] not in lista:
            lista.append(i[0])

    for i in lista:
        new_blabla.drop(new_blabla.loc[new_blabla['DESTINO'] == i].index, inplace=True)

    for i in lista:
        new_blabla.drop(new_blabla.loc[new_blabla['ORIGEN'] == i].index, inplace=True)


    new_blabla.to_csv(f'{os.path.abspath("..")}/ProcessedData/blablacar_basic.csv', index = False)


def main():
   preprocesing()

if __name__=='__main__':
    main()