#!/usr/bin/env python3

import pandas as pd
import os
import json

def introducir_ccaa(df, municipios, ccaa, nombre_columna, type):
    ca_introducir = ['NaN' for i in range(len(municipios))]
    #print(ca_introducir)
    df[nombre_columna] = ca_introducir
    #print(df)

    new_df = pd.DataFrame()
    final_df = pd.DataFrame()

    ya_encontrados = []
    for municipio in municipios:
        #print('entra')
        if municipio[0] not in ya_encontrados:
            ya_encontrados.append(municipio[0])
            if str(municipio[0]) in ccaa.Municipio.values:
                # Añadir la comunidad autonoma de ese municipio
                m = ccaa[ccaa['Municipio'] == municipio[0]] # Fila
                ca = m['Autonomía'].to_numpy().tolist()[0] # Valor
                #mini_df = df[df['ORIGEN'] == municipio[0]]
                # Cambio
                new_df = df[df['ORIGEN'] == municipio[0]]
                #print(new_df)
                new_df = new_df.replace(to_replace ="NaN", value =ca)
                #print(new_df)
                final_df = pd.concat([final_df, new_df])
                
    #print(final_df)
    return final_df

def find_holiday(df, ccaa):
    # Ciudades de origen y destino de los viajes
    origen = df[['ORIGEN']].to_numpy().tolist()
    destino = df[['DESTINO']]

    df = introducir_ccaa(df, origen, ccaa, 'CA_ORIGEN', 'ORIGEN')
    df = introducir_ccaa(df, destino, ccaa, 'CA_DESTINO', 'DESTINO')

def main():
    df = pd.read_csv(f'{os.path.abspath("..")}/ProcessedData/blablacar.csv')
    holidays = pd.read_csv(f'{os.path.abspath("..")}/ProcessedData/calendario.csv')
    ccaa = pd.read_csv(f'{os.path.abspath("..")}/ProcessedData/ccaa.csv')
    ccaa = ccaa.drop(['Unnamed: 0'], axis =1)
    df = df.drop(['Unnamed: 0'], axis =1)
    find_holiday(df, ccaa)

if __name__=='__main__':
    main()