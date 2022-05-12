
#%%
import numpy as np
import pandas as pd

    
df = pd.read_csv(r'C:\Users\neuwirthd\Desktop\Neuer Ordner (5)\daisie-template\apps\new_reports\data\online_retail_II_deutsch.csv')
df = df[0:600]
df.drop_duplicates(inplace = True)
df = df[(df["Menge"]>0)&(df["Preis"]>0)]
df["Rechnungsdatum"] = pd.to_datetime(df["Rechnungsdatum"])
df['Umsatz'] = df['Menge']*df['Preis']
df['Jahr'] = pd.DatetimeIndex(df['Rechnungsdatum']).year
df['Monat'] = pd.DatetimeIndex(df['Rechnungsdatum']).month
df['Wochentag'] = pd.DatetimeIndex(df['Rechnungsdatum']).weekday
df['Tag'] = pd.DatetimeIndex(df['Rechnungsdatum']).day
df['Stunde'] = pd.DatetimeIndex(df['Rechnungsdatum']).hour
df['Kategorie'] = np.random.choice(["Bücher", "Kleidung", "Elektronik", "Lebensmittel", "Haus & Küche"], size=len(df))
df.to_csv(r'C:\Users\neuwirthd\Desktop\Neuer Ordner (5)\daisie-template\apps\new_reports\data\online_retail_ready.csv')

# %%
