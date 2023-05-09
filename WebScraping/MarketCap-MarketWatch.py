#Extrayendo data de capitalización de mercado de empresas desde la página de MarketWatch https://www.marketwatch.com/

#By Brando Huamán www.linkedin.com/in/brandohuaman

#Mensajes comunes al ejecutar la variable response
#<Response [403]>: el sitio web ha detectado que está accediendo a su contenido de manera automatizada y lo haya bloqueado
#<Response [200]>: eso significa que pudo acceder a la página web con éxito.

#Inicio del código
import pandas as pd

# Leer el archivo Excel y almacenarlo en un DataFrame. Servirá para tener la lista de los tickers de acciones que nos interesan.
df = pd.read_excel('S&P BVL Peru General ESG Index.xlsx') 

# Convertir la columna 'Ticker' en una lista
tickers = df['Ticker'].tolist()

tickers

import requests
from bs4 import BeautifulSoup

# Crear una lista vacía para almacenar los resultados de capitalización de mercado
market_cap_list = []

for ticker in tickers:
    # Construir la URL de MarketWatch para cada ticker
    url = f'https://www.marketwatch.com/investing/stock/{ticker}?'
    
    # Hacer una solicitud GET a la página de MarketWatch
    response = requests.get(url)
    
    # Analizar el contenido HTML de la página usando BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar la etiqueta 'small' que contiene el texto 'Market Cap'
    market_cap_label = soup.find('small', text='Market Cap')
    
    # Encontrar la etiqueta 'span' que contiene el valor de la capitalización de mercado
    market_cap_value = market_cap_label.find_next_sibling('span', class_='primary')
    
    # Imprimir el valor de la capitalización de mercado
    print(market_cap_value.text) #print(market_cap_value.text[2:-1]) para eliminar la moneda y unidades
    
    # Agregar el valor de la capitalización de mercado a la lista de resultados
    market_cap_list.append(market_cap_value.text)



# Crear un DataFrame de pandas con los tickers y los valores de capitalización de mercado
df = pd.DataFrame({'Ticker': tickers, 'Market Cap': market_cap_list})
# Imprimir el DataFrame
print(df)

#Extraer la información de moneda, valor y unidad de la columna 'Market Cap'
df[['Moneda', 'Valor', 'Unidad']] = df['Market Cap'].str.extract(r'([S\$]/)?([\d.]+)(B|M|millones|miles de millones)?')

#Rellenar los valores NA de la columna 'Moneda' con el símbolo '$'
df['Moneda'].fillna('$', inplace=True)

df

#Exportar el DataFrame df a un archivo de Excel
df.to_excel('market_cap_peru_esg.xlsx', index=False) 


