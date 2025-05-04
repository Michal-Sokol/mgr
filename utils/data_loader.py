import pandas as pd
import os

def load_data(file):
    """Funkcja wczytująca dane z pliku .csv lub .xlsx i zwracająca DataFrame"""
    name, ext = os.path.splitext(file.name)
    
    if ext == '.csv':
        df = pd.read_csv(file)
    elif ext == '.xlsx':
        xl_file = pd.ExcelFile(file)
        sheet_name = xl_file.sheet_names[0]  # Domyślnie wczytaj pierwszy arkusz
        df = xl_file.parse(sheet_name)
    else:
        raise ValueError('Nieobsługiwany format pliku!')
    
    return df
