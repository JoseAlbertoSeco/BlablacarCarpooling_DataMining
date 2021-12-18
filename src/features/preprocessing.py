#!/usr/bin/env python3

import pandas as pd
import os

def introducir_ccaa(df, municipios, ccaa, nombre_columna, type):
    ca_introducir = ['NaN' for i in range(len(municipios))]
    #print(ca_introducir)
    df[nombre_columna] = ca_introducir
    #print(df)

    new_df = pd.DataFrame()
    final_df = pd.DataFrame()

    ya_encontrados = []
    for municipio in municipios:
        if municipio not in ya_encontrados:
            ya_encontrados.append(municipio)
            if str(municipio) in ccaa.Municipio.values:
                # Añadir la comunidad autonoma de ese municipio
                m = ccaa[ccaa['Municipio'] == municipio] # Fila
                ca = m['Autonomía'].to_numpy().tolist()[0] # Valor
                # Cambio
                new_df = df[df[type] == municipio]
                #print(new_df)
                new_df = new_df.replace(to_replace ="NaN", value =ca)
                #print(new_df)
                final_df = pd.concat([final_df, new_df])
                
    #print(final_df)
    return final_df

def find_holiday(df, ccaa):
    # Ciudades de origen y destino de los viajes
    origen = df['ORIGEN'].tolist()
    df = introducir_ccaa(df, origen, ccaa, 'CA_ORIGEN', 'ORIGEN')

    destino = df['DESTINO'].tolist()
    df = introducir_ccaa(df, destino, ccaa, 'CA_DESTINO', 'DESTINO')

    #print(df)
    df.to_csv(f'{os.path.abspath("..")}/ProcessedData/blablacar_basic.csv', index = False)


def main():
    df = pd.read_csv(f'{os.path.abspath("..")}/ProcessedData/blablacar_basic.csv')
    ccaa = pd.read_csv(f'{os.path.abspath("..")}/ProcessedData/ccaa.csv')
    find_holiday(df, ccaa)

if __name__=='__main__':
    main()