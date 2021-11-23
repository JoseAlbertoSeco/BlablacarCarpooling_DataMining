# -*- coding: utf-8 -*- #

import pandas as pd
import os

''' Basic preprocessing of the dataframe: DATOS_BLABLACAR.txt 

    We only take travel who has more than 0 confirmed seats, and 
    one than 0 offered seats.

    We also get only the travels realized in Spain territory

    The final dataframe can be found in the folder 'ProcessedData'

'''

def preprocesing():
    blabla_data = pd.read_csv(f'{os.path.abspath("..")}\\RawData\\DATOS_BLABLACAR.txt', sep = "|")

    new_blabla = blabla_data[blabla_data['PAIS'] == 'es']

    new_blabla = new_blabla[new_blabla['ASIENTOS_OFERTADOS'] != 0]
    new_blabla =  new_blabla[new_blabla['ASIENTOS_CONFIRMADOS'] != 0]

    portugal_cities = pd.read_excel(f'{os.path.abspath("..")}\\RawData\\portugal.xlsx')

    portugal_cities.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

    cities =  portugal_cities[['Municipios (concelhos)']]
    capitals = portugal_cities[['Ciudad']]
    cities = cities.to_numpy().tolist()
    capitals = capitals.to_numpy().tolist()
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

    new_blabla.to_csv(f'{os.path.abspath("..")}\\ProcessedData\\blablacar.csv')

def main():
    preprocesing()

if __name__=='__main__':
    main()