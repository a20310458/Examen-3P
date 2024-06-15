import pandas as pd
import requests
import hashlib
import time
import sqlite3
import json
# Obtener datos de la API
url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
data = response.json()

# Crear listas para los datos
countries = []
languages = []
hashes = []
times = []

# Procesar datos
for country in data:
    country_name = country.get('name', {}).get('common', 'Unknown')
    language = next(iter(country.get('languages', {}).values()), 'Unknown')
    
    start_time = time.time()
    # Encriptar el nombre del idioma con SHA1
    language_hash = hashlib.sha1(language.encode()).hexdigest()
    end_time = time.time()
    
    processing_time = end_time - start_time
    
    countries.append(country_name)
    languages.append(language)
    hashes.append(language_hash)
    times.append(processing_time)

# Crear DataFrame
df = pd.DataFrame({
    'Country': countries,
    'Language': languages,
    'Language_Hash': hashes,
    'Time': times
})

# Calcular estadísticas de tiempo
total_time = df['Time'].sum()
average_time = df['Time'].mean()
min_time = df['Time'].min()
max_time = df['Time'].max()

print(f"Tiempo total: {total_time} segundos")
print(f"Tiempo promedio: {average_time} segundos")
print(f"Tiempo mínimo: {min_time} segundos")
print(f"Tiempo máximo: {max_time} segundos")

# Guardar en SQLite
conn = sqlite3.connect('countries.db')
df.to_sql('countries', conn, if_exists='replace', index=False)
conn.close()

# Guardar en JSON
df.to_json('data.json', orient='records', lines=True)

print("Datos procesados y guardados correctamente.")