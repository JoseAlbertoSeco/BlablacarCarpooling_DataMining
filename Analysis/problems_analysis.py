# -*- coding: utf-8 -*- #

import pandas as pd
import os

def first_analysis():
    df = pd.read_csv(f'{os.path.abspath("..")}\\RawData\\DATOS_BLABLACAR.txt', sep = "|")
    
    no_seats_oferrs = df[df['ASIENTOS_OFERTADOS'] == 0]
    print('Total rows: :',len(df.index))
    print('Travels without offered seats: ', len(no_seats_oferrs.index),
            '\tPercentage: ', (len(no_seats_oferrs.index)*100)/len(df.index))
    
    empty_tavel =  df[df['ASIENTOS_CONFIRMADOS'] == 0]
    print('Travels with empty seats: ', len(empty_tavel.index),
            '\tPercentage: ', (len(empty_tavel.index)*100)/len(df.index))

    pt = df[df['PAIS'] != 'es']
    print('Data not place in Spain: ', len(pt.index),
            '\tPercentage: ', (len(pt.index)*100)/len(df.index))

def main():
    first_analysis()

if __name__=='__main__':
    main()