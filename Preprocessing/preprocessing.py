import pandas as pd
import os

def find_holiday(df, holidays):
    # Nombre de todas las columnas del calendario
    festivos = holidays.columns
    festivos = festivos.to_numpy().tolist()
    
    holidays = holidays.drop(holidays.columns[[0]], axis='columns')
    for (label, content) in holidays.iteritems():
        print('CA: ', label)
        print('Festivo: ', content.values)

def main():
    df = pd.read_csv(f'{os.path.abspath("..")}/ProcessedData/blablacar.csv')
    holidays = pd.read_csv(f'{os.path.abspath("..")}/ProcessedData/calendario.csv')

    find_holiday(df, holidays)

if __name__=='__main__':
    main()