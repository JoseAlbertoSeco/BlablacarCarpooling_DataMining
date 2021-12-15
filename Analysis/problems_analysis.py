#!/usr/bin/env python3

import pandas as pd
import os

''' 
    Primer acercamiento a los datos, realizamos un primer analisis de datos y una primera toma de
    contacto con los problemas encontrados en ellos 

'''

def first_analysis():

    df = pd.read_csv(f'{os.path.abspath("..")}/RawData/DATOS_BLABLACAR.txt', sep = "|")

    print('Columnas y tipos de columnas: \n', df.dtypes)
    print('----------------------------------------------------------------------')
    print('Descripción general: \n',df.describe())
    print('----------------------------------------------------------------------')
    print('Valores nulos: ', df.isnull().values.any())
    print('Número total de valores nulos por columna: \n', df.isnull().sum())
    print('----------------------------------------------------------------------')
    print('Filas y columnas iniciales: ', df.shape)
    print('----------------------------------------------------------------------')

    print('Una vez comprobados los valores extraeremos el porcentaje IMP_KM de valores nulos:\n ', (df['IMP_KM'].isnull().sum())*100/len(df.index), '%')

    print('----------------------------------------------------------------------')
    no_seats_oferrs = df[df['ASIENTOS_OFERTADOS'] == 0]
    print('Viajes sin asientos ofertados: ', len(no_seats_oferrs.index),
        '\tPorcentaje: ', (len(no_seats_oferrs.index)*100)/len(df.index),'%')
    
    empty_tavel =  df[df['ASIENTOS_CONFIRMADOS'] == 0]
    print('Viajes sin asientos confirmados: ', len(empty_tavel.index),
        '\tPorcentaje: ', (len(empty_tavel.index)*100)/len(df.index),'%')

    pt = df[df['PAIS'] != 'es']
    print('Viajes que inician o acaban en Portugal: ', len(pt.index),
            '\tPorcentaje: ', (len(pt.index)*100)/len(df.index),'%')

def main():
    first_analysis()

if __name__=='__main__':
    main()
    