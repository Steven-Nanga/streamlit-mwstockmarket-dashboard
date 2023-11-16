import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

url = "https://mse.co.mw/market/mainboard"

# Fetch the HTML content from the URL
response = requests.get(url)
html = response.text

# Parse the HTML content
soup = BeautifulSoup(html, 'html.parser')

# Find the table with the specified class
table = soup.find('table', class_='table')

# Check if the table was found
if table:
    # Extract data from the table
    data = []
    for row in table.find_all('tr')[1:-1]:  # Exclude the header and footer rows
        columns = row.find_all(['td', 'th'])
        symbol = columns[0].find('a').text.strip()
        open_price = columns[1].text.strip()
        close_price = columns[2].text.strip()
        percent_change = columns[3].text.strip()
        volume = columns[4].text.strip().replace(',', '')
        turnover = columns[5].text.strip().replace(',', '')

        data.append({
            'Symbol': symbol,
            'Open Price': open_price,
            'Close Price': close_price,
            'Percent Change': percent_change,
            'Volume': volume,
            'Turnover': turnover,
        })

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Add a column for the collection date
    df['Date Collected'] = datetime.now()

    # Print the DataFrame
    print(df)
else:
    print("Table not found.")
